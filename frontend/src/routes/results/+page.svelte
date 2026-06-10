<script lang="ts">
  import SocialCardExport from "../../lib/components/SocialCardExport.svelte";

  export let data;

  $: leader =
    data.scoreboard.human_points === data.scoreboard.ai_points
      ? "TIE"
      : data.scoreboard.human_points > data.scoreboard.ai_points
        ? "HUMAN LEADS"
        : "AI LEADS";
</script>

<section class="glass-card board neon-primary">
  <p class="mono">LIVE SCOREBOARD LEADER</p>
  <h1>{leader}</h1>
  <div class="line"></div>
  <div class="score-row">
    <div>
      <p>Human</p>
      <strong>{data.scoreboard.human_points}</strong>
      <small>{data.scoreboard.human_exact_scores} exacts</small>
    </div>
    <div>
      <p>AI</p>
      <strong>{data.scoreboard.ai_points}</strong>
      <small>{data.scoreboard.ai_exact_scores} exacts</small>
    </div>
  </div>
</section>

<SocialCardExport />

<section class="results-list">
  <h2>Completed Matches</h2>
  {#if data.completed.length === 0}
    <div class="glass-card row">No completed matches yet.</div>
  {:else}
    {#each data.completed as match}
      <div class="glass-card row pulse-award">
        <div>
          <p class="teams">{match.team_a_code} vs {match.team_b_code}</p>
          <p class="meta">{match.team_a_name} vs {match.team_b_name}</p>
        </div>
        <p class="display score">{match.actual_score_a} : {match.actual_score_b}</p>
      </div>
    {/each}
  {/if}
</section>

<style>
  .board {
    padding: 1rem;
    margin-bottom: 1rem;
  }
  h1 {
    margin: 0.2rem 0 0.6rem;
    font-size: clamp(1.8rem, 4vw, 2.8rem);
  }
  .line {
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    margin: 0.5rem 0 0.8rem;
  }
  .score-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
  strong {
    display: block;
    font-size: 2rem;
    font-family: "Archivo Narrow", sans-serif;
  }
  small,
  .meta,
  .mono {
    color: var(--on-surface-variant);
  }
  .results-list {
    display: grid;
    gap: 0.7rem;
  }
  .row {
    padding: 0.9rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .teams {
    margin: 0;
    font-family: "Archivo Narrow", sans-serif;
    font-size: 1.2rem;
  }
  .meta {
    margin: 0.1rem 0 0;
  }
  .score {
    margin: 0;
    font-size: 2rem;
  }

  @keyframes award {
    0% {
      box-shadow: 0 0 0 rgba(0, 219, 233, 0);
    }
    50% {
      box-shadow: 0 0 20px rgba(0, 219, 233, 0.18);
    }
    100% {
      box-shadow: 0 0 0 rgba(0, 219, 233, 0);
    }
  }

  .pulse-award {
    animation: award 1.8s ease-in-out infinite;
  }
</style>
