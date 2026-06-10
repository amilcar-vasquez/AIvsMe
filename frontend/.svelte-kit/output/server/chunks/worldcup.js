//#region src/lib/api/client.ts
var API_BASE_URL = "http://localhost:8000/api";
async function apiGet(path, fetchFn) {
	const response = await fetchFn(`${API_BASE_URL}${path}`);
	if (!response.ok) throw new Error(`GET ${path} failed: ${response.status}`);
	return response.json();
}
async function apiPost(path, payload, fetchFn) {
	const response = await fetchFn(`${API_BASE_URL}${path}`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(payload)
	});
	if (!response.ok) throw new Error(`POST ${path} failed: ${response.status}`);
	return response.json();
}
//#endregion
//#region src/lib/api/worldcup.ts
var worldCupApi = {
	getScoreboard(fetchFn) {
		return apiGet("/scoreboard/", fetchFn);
	},
	getUpcomingMatches(fetchFn) {
		return apiGet("/matches/upcoming/", fetchFn);
	},
	getCompletedMatches(fetchFn) {
		return apiGet("/matches/completed/", fetchFn);
	},
	getMatch(matchId, fetchFn) {
		return apiGet(`/matches/${matchId}/`, fetchFn);
	},
	getMatchPredictions(matchId, fetchFn) {
		return apiGet(`/matches/${matchId}/predictions/`, fetchFn);
	},
	listPredictions(fetchFn) {
		return apiGet("/predictions/", fetchFn);
	},
	createPrediction(payload, fetchFn) {
		return apiPost("/predictions/", payload, fetchFn);
	},
	setMatchResult(matchId, payload, fetchFn) {
		return apiPost(`/matches/${matchId}/set-result/`, payload, fetchFn);
	}
};
//#endregion
export { worldCupApi as t };
