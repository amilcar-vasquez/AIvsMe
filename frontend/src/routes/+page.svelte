<script lang="ts">
  import { fly } from "svelte/transition";
  import ScoreboardHero from "../lib/components/ScoreboardHero.svelte";
  import UpcomingMatches from "../lib/components/UpcomingMatches.svelte";

  export let data;

  $: humanRate = data.scoreboard.total_matches
    ? Math.round((data.scoreboard.human_exact_scores / data.scoreboard.total_matches) * 100)
    : 0;
  $: aiRate = data.scoreboard.total_matches
    ? Math.round((data.scoreboard.ai_exact_scores / data.scoreboard.total_matches) * 100)
    : 0;

  const stats = [
    { label: "HUMAN EXACT SCORE RATE", value: humanRate, unit: "%" },
    { label: "AI EXACT SCORE RATE", value: aiRate, unit: "%" },
    { label: "TOTAL MATCHES SCORED", value: data.scoreboard.total_matches, unit: "" }
  ];
</script>

<ScoreboardHero scoreboard={data.scoreboard} />

<section class="glass-card neon-secondary stats">
  {#each stats as stat, i (stat.label)}
    <div in:fly={{ y: 20, duration: 300, delay: i * 80 }}>
      <p class="mono">{stat.label}</p>
      <h3>{stat.value}{stat.unit}</h3>
    </div>
  {/each}
</section>

<UpcomingMatches matches={data.upcoming} />

<style>
  .stats {
    padding: 1rem;
    margin-bottom: 1.2rem;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 0.8rem;
  }
  p {
    margin: 0;
    color: var(--on-surface-variant);
    font-size: 0.75rem;
  }
  h3 {
    margin: 0.25rem 0 0;
    font-size: 1.6rem;
  }
</style>
