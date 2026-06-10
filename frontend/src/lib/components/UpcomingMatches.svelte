<script lang="ts">
  import { fly } from "svelte/transition";
  import type { Match } from "../types/domain";

  export let matches: Match[];

  const dateFmt = new Intl.DateTimeFormat(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric"
  });

  const timeFmt = new Intl.DateTimeFormat(undefined, {
    hour: "2-digit",
    minute: "2-digit"
  });

  $: sorted = [...matches].sort(
    (a, b) => new Date(a.kickoff_time).getTime() - new Date(b.kickoff_time).getTime()
  );

  $: firstMatch = sorted[0] ?? null;

  $: grouped = sorted.reduce<{ dayLabel: string; items: Match[] }[]>((acc, match) => {
    const label = dateFmt.format(new Date(match.kickoff_time));
    const existing = acc.find((entry) => entry.dayLabel === label);
    if (existing) {
      existing.items.push(match);
      return acc;
    }
    acc.push({ dayLabel: label, items: [match] });
    return acc;
  }, []);
</script>

<section class="list">
  <div class="title-row">
    <h2>Upcoming: Tomorrow + 3 Days</h2>
    <p class="mono hint">Tap any match to predict</p>
  </div>

  {#if firstMatch}
    <a class="glass-card neon-primary first-cta" href={`/matches/${firstMatch.id}`}>
      <div>
        <p class="mono cta-label">FIRST KICKOFF</p>
        <h3>{firstMatch.team_a_name} vs {firstMatch.team_b_name}</h3>
        <p class="meta">{firstMatch.stadium} • {dateFmt.format(new Date(firstMatch.kickoff_time))} {timeFmt.format(new Date(firstMatch.kickoff_time))}</p>
      </div>
      <span class="cta-action">Predict</span>
    </a>
  {/if}

  {#if matches.length === 0}
    <div class="glass-card item">No upcoming matches yet.</div>
  {:else}
    {#each grouped as dayBlock, dayIndex}
      <section class="day-block" in:fly={{ y: 14, duration: 260, delay: dayIndex * 60 }}>
        <p class="mono day-label">{dayBlock.dayLabel}</p>
        {#each dayBlock.items as match}
          <a class="glass-card item" href={`/matches/${match.id}`}>
            <div>
              <p class="teams">{match.team_a_code} vs {match.team_b_code}</p>
              <p class="meta">{match.team_a_name} vs {match.team_b_name}</p>
              <p class="meta stadium">{match.stadium}</p>
            </div>
            <p class="mono kickoff">{timeFmt.format(new Date(match.kickoff_time))}</p>
          </a>
        {/each}
      </section>
    {/each}
  {/if}
</section>

<style>
  .list {
    display: grid;
    gap: 0.75rem;
  }
  .title-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 0.6rem;
  }
  h2 {
    margin: 0.5rem 0;
    font-size: 1.6rem;
  }
  .hint {
    margin: 0;
    color: var(--on-surface-variant);
    font-size: 0.75rem;
  }
  .first-cta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    text-decoration: none;
    color: inherit;
  }
  .cta-label {
    color: var(--primary-fixed);
    margin: 0;
    font-size: 0.72rem;
  }
  .first-cta h3 {
    margin: 0.2rem 0;
    font-size: 1.2rem;
  }
  .cta-action {
    border: 1px solid var(--primary-fixed-dim);
    padding: 0.45rem 0.8rem;
    border-radius: 999px;
    font-family: "JetBrains Mono", monospace;
    font-size: 0.75rem;
    color: var(--primary-fixed);
  }
  .day-block {
    display: grid;
    gap: 0.5rem;
  }
  .day-label {
    margin: 0.2rem 0;
    color: var(--secondary-fixed);
    font-size: 0.8rem;
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
  .stadium {
    font-size: 0.8rem;
  }
  .kickoff {
    color: var(--primary-fixed);
    font-size: 0.8rem;
  }
  @media (max-width: 700px) {
    .title-row {
      flex-direction: column;
      align-items: flex-start;
    }
    .item {
      align-items: flex-start;
      flex-direction: column;
      gap: 0.35rem;
    }
  }
</style>
