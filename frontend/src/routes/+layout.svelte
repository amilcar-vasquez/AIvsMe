<script lang="ts">
  import "../app.css";
  import { onMount } from "svelte";

  let mounted = false;

  onMount(() => {
    mounted = true;
  });
</script>

<header class="topbar">
  <div class="container row">
    <a class="brand" href="/">AI vs ME - World Cup Prediction Challenge</a>
    <nav>
      <a href="/">Predict</a>
      <a href="/results">Results</a>
    </nav>
  </div>
</header>

<main class="container main" class:animate-in={mounted}>
  <slot />
</main>

<style>
  .topbar {
    position: sticky;
    top: 0;
    z-index: 10;
    backdrop-filter: blur(12px);
    background: rgba(5, 5, 5, 0.8);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }
  .row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    min-height: 64px;
  }
  .brand {
    color: var(--primary-fixed);
    text-decoration: none;
    font-family: "Archivo Narrow", sans-serif;
    font-weight: 700;
    font-size: 1.5rem;
  }
  nav {
    display: flex;
    gap: 1rem;
  }
  nav a {
    color: var(--on-surface-variant);
    text-decoration: none;
    font-weight: 600;
  }
  nav a:hover {
    color: var(--on-surface);
  }
  .main {
    padding: 1rem 0 2rem;
  }
</style>
