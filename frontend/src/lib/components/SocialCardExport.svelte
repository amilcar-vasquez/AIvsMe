<script lang="ts">
  const API_BASE_URL =
    (import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "http://localhost:8000/api") +
    "/scoreboard/social-card/";

  let ratio: "9:16" | "16:9" | "1:1" = "9:16";

  $: cardUrl = `${API_BASE_URL}?ratio=${encodeURIComponent(ratio)}`;

  async function copyLink() {
    await navigator.clipboard.writeText(cardUrl);
  }
</script>

<section class="glass-card exporter">
  <div class="head">
    <h3>Social Card Export</h3>
    <p class="mono">Shorts/TikTok/Stories ready</p>
  </div>

  <div class="controls">
    <button class:active={ratio === "9:16"} on:click={() => (ratio = "9:16")}>9:16</button>
    <button class:active={ratio === "16:9"} on:click={() => (ratio = "16:9")}>16:9</button>
    <button class:active={ratio === "1:1"} on:click={() => (ratio = "1:1")}>1:1</button>
  </div>

  <a class="preview" href={cardUrl} target="_blank" rel="noreferrer">
    <img src={cardUrl} alt="AI vs Me social scoreboard card" loading="lazy" />
  </a>

  <div class="actions">
    <a class="btn btn-primary" href={cardUrl} download={`ai-vs-me-${ratio}.svg`}>Download SVG</a>
    <button class="btn btn-secondary" on:click={copyLink}>Copy Share Link</button>
  </div>
</section>

<style>
  .exporter {
    padding: 1rem;
    display: grid;
    gap: 0.8rem;
  }
  h3 {
    margin: 0;
    font-size: 1.35rem;
  }
  .head p {
    margin: 0.2rem 0 0;
    color: var(--on-surface-variant);
    font-size: 0.78rem;
  }
  .controls {
    display: flex;
    gap: 0.5rem;
  }
  .controls button {
    border: 1px solid var(--outline-variant);
    background: transparent;
    color: var(--on-surface-variant);
    border-radius: 999px;
    padding: 0.35rem 0.8rem;
    cursor: pointer;
    font-weight: 700;
  }
  .controls button.active {
    border-color: var(--primary-fixed-dim);
    color: var(--primary-fixed);
    box-shadow: 0 0 16px rgba(0, 219, 233, 0.2);
  }
  .preview {
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    overflow: hidden;
    display: block;
    background: rgba(255, 255, 255, 0.03);
  }
  img {
    width: 100%;
    max-height: 520px;
    object-fit: contain;
    display: block;
  }
  .actions {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
  }
</style>
