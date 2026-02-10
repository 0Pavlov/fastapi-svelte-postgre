<script lang="ts">
    import { onMount } from 'svelte';
    // Health check var
    let hello = $state('loading...');
    const API_BASE_URL = 'http://localhost:8000';

    async function apiRequest<T>(url: string, options?: RequestInit): Promise<T> {
        const res = await fetch(url, options);
        if (!res.ok) {
            // This handles the 500 error gracefully in console, though backend still needs fix
            const errorText = await res.text();
            throw new Error(`API Error ${res.status}: ${errorText}`);
        }
        return res.json();
    }

    async function fetchServer() {
        try {
            const data = await apiRequest<{status: string}>(`${API_BASE_URL}/`);
            hello = data.status;
        } catch (e) {
            hello = "Backend Offline";
        }
    }

    onMount(() => {
        fetchServer();
	});
</script>
<span>{ hello }</span>
