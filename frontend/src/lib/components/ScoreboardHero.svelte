<script lang="ts">
  import { onMount } from "svelte";
  import { scale } from "svelte/transition";
  import type { Scoreboard } from "../types/domain";

  export let scoreboard: Scoreboard;

  let displayedHumanPoints = 0;
  let displayedAIPoints = 0;

  $: lead = displayedAIPoints - displayedHumanPoints;
  $: momentum = lead === 0 ? "TIED" : lead > 0 ? "AI MOMENTUM" : "HUMAN MOMENTUM";

  onMount(() => {
    // Animate count-up over 1s
    const duration = 1000;
    const startTime = Date.now();

    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);

      displayedHumanPoints = Math.floor(scoreboard.human_points * progress);
      displayedAIPoints = Math.floor(scoreboard.ai_points * progress);

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        // Ensure final values are exact
        displayedHumanPoints = scoreboard.human_points;
        displayedAIPoints = scoreboard.ai_points;
      }
    };

    animate();
  });
</script>

<section class="glass-card neon-primary hero">
  <div>
    <p class="mono label">LIVE TOURNAMENT STATUS</p>
    <h1>World Cup Arena</h1>
    <p class="momentum" transition:scale={{ duration: 200 }}>{momentum}</p>
  </div>

  <div class="score">
    <div>
      <p class="mono human">HUMAN</p>
      <span class="display">{displayedHumanPoints}</span>
    </div>
    <div class="vs display">VS</div>
    <div>
      <p class="mono ai">AI</p>
      <span class="display">{displayedAIPoints}</span>
    </div>
  </div>
</section>

<style>
  .hero {
    padding: 1.2rem;
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin: 1.2rem 0;
    flex-wrap: wrap;
  }
  .label {
    color: var(--secondary-fixed);
    font-size: 0.75rem;
  }
  h1 {
    margin: 0.2rem 0;
    font-size: clamp(1.7rem, 3vw, 2.8rem);
  }
  .momentum {
    color: var(--on-surface-variant);
    margin: 0;
  }
  .score {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  .human {
    color: var(--secondary-fixed);
  }
  .ai {
    color: var(--primary-fixed);
  }
  .vs {
    opacity: 0.4;
  }
  span {
    font-size: 2.2rem;
  }
</style>
