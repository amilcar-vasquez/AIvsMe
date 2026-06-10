<script lang="ts">
  import { fly } from "svelte/transition";
  import type { Match } from "../types/domain";

  export let matches: Match[];
</script>

<section class="list">
  <h2>Upcoming Matches</h2>
  {#if matches.length === 0}
    <div class="glass-card item">No upcoming matches yet.</div>
  {:else}
    {#each matches as match, i}
      <a 
        class="glass-card item" 
        href={`/matches/${match.id}`}
        in:fly={{ y: 16, duration: 280, delay: i * 60 }}
      >
        <div>
          <p class="teams">{match.team_a_code} vs {match.team_b_code}</p>
          <p class="meta">{match.team_a_name} vs {match.team_b_name}</p>
        </div>
        <p class="mono kickoff">{new Date(match.kickoff_time).toLocaleString()}</p>
      </a>
    {/each}
  {/if}
</section>

<style>
  .list {
    display: grid;
    gap: 0.75rem;
  }
  h2 {
    margin: 0.5rem 0;
    font-size: 1.6rem;
  }
  .item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    color: inherit;
    text-decoration: none;
  }
  .teams {
    margin: 0;
    font-size: 1.15rem;
    font-family: "Archivo Narrow", sans-serif;
  }
  .meta {
    margin: 0.2rem 0 0;
    color: var(--on-surface-variant);
    font-size: 0.9rem;
  }
  .kickoff {
    color: var(--primary-fixed);
    font-size: 0.8rem;
  }
</style>
