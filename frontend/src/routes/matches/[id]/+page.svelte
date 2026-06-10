<script lang="ts">
  import { onMount } from "svelte";
  import { fade, fly } from "svelte/transition";
  import { worldCupApi } from "../../../lib/api/worldcup";

  export let data;

  let scoreA = data.humanPrediction?.predicted_score_a ?? 0;
  let scoreB = data.humanPrediction?.predicted_score_b ?? 0;
  let reasoning = data.humanPrediction?.reasoning ?? "";
  let message = "";

  // AI State Machine
  type AIState = "idle" | "thinking" | "challenge" | "revealed";
  let aiState: AIState = data.aiPrediction ? "revealed" : "idle";

  // AI Thinking animation
  let thinkingDots = "▪";
  let thinkingInterval: number | null = null;
  let typewriterText = "";
  let typewriterIndex = 0;
  let typewriterInterval: number | null = null;

  // Score countdown from placeholder to revealed
  let displayScoreA = 0;
  let displayScoreB = 0;
  let countdownInterval: number | null = null;

  // Shared reasoning from AI prediction
  let aiReasoningText = data.aiPrediction?.reasoning ?? "";
  let displayedAIScore = data.aiPrediction?.predicted_score_a ?? 0;
  let displayedAIScoreB = data.aiPrediction?.predicted_score_b ?? 0;
  let aiConfidence = data.aiPrediction?.confidence_score ?? 0;
  let displayedConfidence = 0;

  // Animate thinking dots
  function startThinkingAnimation() {
    let dotCount = 0;
    thinkingInterval = window.setInterval(() => {
      dotCount = (dotCount + 1) % 4;
      thinkingDots = "▪".repeat(dotCount || 1);
    }, 600);
  }

  function stopThinkingAnimation() {
    if (thinkingInterval !== null) {
      clearInterval(thinkingInterval);
      thinkingInterval = null;
    }
  }

  // Typewriter effect for reasoning
  function startTypewriter(text: string) {
    typewriterText = "";
    typewriterIndex = 0;
    typewriterInterval = window.setInterval(() => {
      if (typewriterIndex < text.length) {
        typewriterText += text[typewriterIndex];
        typewriterIndex++;
      } else {
        stopTypewriter();
      }
    }, 25);
  }

  function stopTypewriter() {
    if (typewriterInterval !== null) {
      clearInterval(typewriterInterval);
      typewriterInterval = null;
    }
  }

  // Animate score countdown from -- to actual value
  function startScoreCountdown(finalA: number, finalB: number) {
    displayScoreA = 0;
    displayScoreB = 0;
    let aReached = false;
    let bReached = false;

    countdownInterval = window.setInterval(() => {
      if (displayScoreA < finalA) {
        displayScoreA++;
      } else {
        aReached = true;
      }
      if (displayScoreB < finalB) {
        displayScoreB++;
      } else {
        bReached = true;
      }

      if (aReached && bReached) {
        if (countdownInterval !== null) {
          clearInterval(countdownInterval);
          countdownInterval = null;
        }
      }
    }, 40);
  }

  // Animate confidence bar
  function startConfidenceBar(target: number) {
    displayedConfidence = 0;
    const increment = target / 20; // 20 steps
    let steps = 0;
    const interval = window.setInterval(() => {
      displayedConfidence = Math.min(target, displayedConfidence + increment);
      steps++;
      if (steps >= 20) {
        displayedConfidence = target;
        clearInterval(interval);
      }
    }, 40);
  }

  async function submitPrediction() {
    try {
      // Lock the panel immediately
      aiState = "thinking";
      startThinkingAnimation();

      // Submit human prediction
      await worldCupApi.createPrediction(
        {
          match: data.match.id,
          predictor_type: "human",
          predicted_score_a: Number(scoreA),
          predicted_score_b: Number(scoreB),
          confidence_score: 75,
          reasoning
        },
        fetch
      );

      // Wait a moment, then re-fetch to get fresh AI prediction
      await new Promise(resolve => setTimeout(resolve, 500));
      const updated = await worldCupApi.getMatchPredictions(data.match.id, fetch);
      const aiPred = updated.find((p: any) => p.predictor_type === "ai");

      if (aiPred) {
        stopThinkingAnimation();
        aiReasoningText = aiPred.reasoning;
        displayedAIScore = aiPred.predicted_score_a;
        displayedAIScoreB = aiPred.predicted_score_b;
        aiConfidence = aiPred.confidence_score;

        // Cinematic reveal: flash + challenge accepted + countdown + typewriter
        aiState = "challenge";
        startScoreCountdown(displayedAIScore, displayedAIScoreB);
        startConfidenceBar(aiConfidence);

        // After challenge flash settles (1.5s), transition to revealed
        await new Promise(resolve => setTimeout(resolve, 1500));
        aiState = "revealed";
        startTypewriter(aiReasoningText);

        message = "AI has accepted your challenge!";
      }
    } catch (error) {
      stopThinkingAnimation();
      aiState = data.aiPrediction ? "revealed" : "idle";
      message = error instanceof Error ? error.message : "Failed to submit prediction.";
    }
  }

  onMount(() => {
    // If AI prediction already loaded, start typewriter
    if (aiState === "revealed" && aiReasoningText) {
      startTypewriter(aiReasoningText);
    }
  });
</script>

<section class="header">
  <p class="mono stage">{data.match.stage.replaceAll("_", " ")}</p>
  <h1 in:fly={{ y: -20, duration: 300 }}>{data.match.team_a_name} vs {data.match.team_b_name}</h1>
  <p class="mono">Kickoff: {new Date(data.match.kickoff_time).toLocaleString()}</p>
</section>

<section class="duel-grid">
  <article
    class="glass-card neon-secondary panel"
    class:locked-state={aiState === "thinking"}
    in:fly={{ x: -30, duration: 400, delay: 100 }}
  >
    <h2>Human Prediction</h2>
    <div class="inputs">
      <label>
        {data.match.team_a_code}
        <input type="number" min="0" bind:value={scoreA} disabled={aiState === "thinking"} />
      </label>
      <span>:</span>
      <label>
        {data.match.team_b_code}
        <input type="number" min="0" bind:value={scoreB} disabled={aiState === "thinking"} />
      </label>
    </div>
    <textarea
      bind:value={reasoning}
      rows="4"
      placeholder="Add your match rationale"
      disabled={aiState === "thinking"}
    ></textarea>
    <button class="btn btn-secondary" on:click={submitPrediction} disabled={aiState === "thinking"}>
      {aiState === "thinking" ? "AI THINKING..." : "Save Prediction"}
    </button>
  </article>

  <article
    class="glass-card neon-primary panel ai-panel"
    class:thinking={aiState === "thinking"}
    class:challenge={aiState === "challenge"}
    in:fly={{ x: 30, duration: 400, delay: 250 }}
  >
    <h2>AI Prediction</h2>

    {#if aiState === "idle"}
      <p class="idle-placeholder">AI prediction will auto-generate after your human pick is submitted.</p>
    {/if}

    {#if aiState === "thinking"}
      <div class="thinking-content">
        <p class="thinking-header">ANALYZING MATCH DATA <span class="thinking-indicator"></span></p>
        <div class="dots-animation">
          <div class="dot-row" style="animation-delay: 0ms">▪</div>
          <div class="dot-row" style="animation-delay: 150ms">▪</div>
          <div class="dot-row" style="animation-delay: 300ms">▪</div>
        </div>
        <p class="mono consulting">CONSULTING AI ENGINE</p>
      </div>
    {/if}

    {#if aiState === "challenge" || aiState === "revealed"}
      <div key={aiState} class:settling={aiState === "revealed"}>
        <p class="display score challenge-score">{displayScoreA} : {displayScoreB}</p>
        <div class="confidence-container">
          <p class="mono confidence">CONFIDENCE</p>
          <div class="confidence-bar">
            <div class="confidence-fill" style="width: {displayedConfidence}%"></div>
          </div>
          <p class="confidence-value">{Math.round(displayedConfidence)}%</p>
        </div>
        {#if aiState === "challenge"}
          <p class="challenge-header">CHALLENGE ACCEPTED</p>
        {/if}
        {#if aiState === "revealed"}
          <p class="reasoning-text">{typewriterText}<span class="cursor">{typewriterIndex < aiReasoningText.length ? '▋' : ''}</span></p>
        {/if}
      </div>
    {/if}
  </article>
</section>

{#if message}
  <p class="toast" in:fade={{ duration: 300 }}>{message}</p>
{/if}

<style>
  .header {
    margin-bottom: 1rem;
  }
  h1 {
    margin: 0.2rem 0;
    font-size: clamp(1.5rem, 3vw, 2.4rem);
  }
  .stage {
    color: var(--primary-fixed);
  }
  .duel-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
  }
  .panel {
    padding: 1rem;
    display: grid;
    gap: 0.75rem;
  }
  .inputs {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 0.7rem;
  }
  label {
    display: grid;
    gap: 0.35rem;
    font-size: 0.8rem;
  }
  input,
  textarea {
    width: 100%;
    border: 1px solid var(--outline-variant);
    background: var(--surface-container-low);
    color: var(--on-surface);
    border-radius: 10px;
    padding: 0.6rem;
    transition: all 0.2s ease;
  }
  input:disabled,
  textarea:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  .ai-panel {
    background: linear-gradient(160deg, rgba(0, 219, 233, 0.08), rgba(0, 0, 0, 0.05));
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  .ai-panel.thinking {
    border-color: var(--primary-fixed);
    background: linear-gradient(160deg, rgba(0, 219, 233, 0.15), rgba(0, 0, 0, 0.05));
  }
  .ai-panel.challenge {
    animation: challenge-flash 1.5s ease-in-out 1;
  }
  .score {
    font-size: 2.4rem;
    margin: 0;
    font-family: "Archivo Narrow", sans-serif;
  }
  .challenge-score {
    font-size: clamp(2rem, 8vw, 3.2rem);
  }
  .confidence {
    color: var(--primary-fixed);
    margin: 0;
  }
  .toast {
    margin-top: 1rem;
    color: var(--secondary-fixed);
  }

  /* THINKING STATE STYLES */

  .idle-placeholder {
    color: var(--on-surface-variant);
    line-height: 1.6;
  }

  .thinking-content {
    display: grid;
    gap: 1.2rem;
    align-items: center;
  }

  .thinking-header {
    font-size: 1rem;
    color: var(--primary-fixed);
    margin: 0;
    font-weight: 600;
    letter-spacing: 0.1em;
  }

  .thinking-indicator {
    display: inline-block;
    width: 0.4em;
    height: 1em;
    background: var(--primary-fixed);
    border-radius: 2px;
    animation: cursor-blink 1s step-end infinite;
    margin-left: 0.2em;
  }

  .dots-animation {
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    height: 24px;
    align-items: center;
  }

  .dot-row {
    font-size: 1.4rem;
    color: var(--primary-fixed);
    animation: dot-scroll 0.8s ease-in-out infinite;
  }

  .consulting {
    text-align: center;
    color: var(--on-surface-variant);
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    margin: 0;
  }

  /* CHALLENGE & REVEALED STATE STYLES */

  .challenge-header {
    font-size: 1.4rem;
    color: var(--secondary-fixed);
    text-align: center;
    margin: 0.5rem 0 0;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-weight: 700;
    animation: pulse-challenge 0.6s ease-out;
  }

  @keyframes pulse-challenge {
    from {
      transform: scale(0.8);
      opacity: 0;
    }
    to {
      transform: scale(1);
      opacity: 1;
    }
  }

  .confidence-container {
    display: grid;
    gap: 0.5rem;
  }

  .confidence-bar {
    height: 6px;
    background: var(--surface-container-high);
    border-radius: 999px;
    overflow: hidden;
    border: 1px solid var(--outline-variant);
  }

  .confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary-fixed-dim), var(--primary-fixed));
    transition: width 800ms cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .confidence-value {
    text-align: right;
    font-size: 0.75rem;
    color: var(--primary-fixed);
    margin: 0;
    font-weight: 700;
  }

  .reasoning-text {
    color: var(--on-surface);
    line-height: 1.6;
    margin: 0.8rem 0 0;
    font-size: 0.95rem;
  }

  .cursor {
    display: inline-block;
    animation: cursor-blink 1s step-end infinite;
    color: var(--primary-fixed);
  }

  .settling {
    animation: fade-in 0.4s ease-out;
  }

  @keyframes fade-in {
    from {
      opacity: 0.7;
    }
    to {
      opacity: 1;
    }
  }
</style>
