<script lang="ts">
	import { onMount } from 'svelte';
	import { Spinner } from "$lib/components/ui/spinner";
	import { Button } from "$lib/components/ui/button";
	import AddTodoCard from "./AddTodoCard.svelte";
    import * as Card from "$lib/components/ui/card";

    import { ModeWatcher } from "mode-watcher";
    import SunIcon from "@lucide/svelte/icons/sun";
    import MoonIcon from "@lucide/svelte/icons/moon";
    import { toggleMode } from "mode-watcher";

    // Standard const object for Svelte
    export const PriorityEnum = {
        HIGH: 1,
        MEDIUM: 2,
        LOW: 3
    } as const;

    export interface TodoBase {
        todo_name: string;
        todo_description: string;
        todo_priority: number;
    }

    export interface TodoCreate extends TodoBase {}

    export interface Todo extends TodoBase {
        todo_id: number;
        editing?: boolean; // UI state
    }

    export interface TodoUpdate {
        todo_name?: string;
        todo_description?: string;
        todo_priority?: number; 
    }

    // Should be changed in prod
    // For dev purposes the localhost should be changed to a an ip of the machine
    // that runs the backend
    const API_BASE_URL = '/api';

    let hello = $state('loading...');
    let todos = $state<Todo[]>([]);
    let intervalId: number | null = null;
    let isPollingActive = $state(false);
    const POLLING_INTERVAL = 3000;

    const priorityLabels: Record<number, string> = {
        1: "High",
        2: "Medium",
        3: "Low"
    };

    async function apiRequest<T>(url: string, options?: RequestInit): Promise<T> {
        const res = await fetch(url, options);
        if (!res.ok) {
            // This handles the 500 error gracefully in console, though backend still needs fix
            const errorText = await res.text();
            throw new Error(`API Error ${res.status}: ${errorText}`);
        }
        return res.json();
    }

    async function getTodos(firstN?: number): Promise<void> {
        const url = firstN ? `${API_BASE_URL}/todos?first_n=${firstN}` : `${API_BASE_URL}/todos`;
        try {
            todos = await apiRequest<Todo[]>(url);
        } catch (e) {
            console.error("Polling error:", e);
        }
    }

    async function deleteTodo(id: number): Promise<void> {
        try {
            await apiRequest(`${API_BASE_URL}/todos/${id}`, { method: 'DELETE' });
            await getTodos();
        } catch (e) {
            alert("Failed to delete todo");
        }
    }

    async function updateTodo(id: number, updatedTodo: TodoUpdate): Promise<void> {
        try {
            await apiRequest(`${API_BASE_URL}/todos/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedTodo),
            });
            await getTodos();
        } catch (e) {
            console.error(e);
            alert("Update failed. Check backend console for attribute error.");
        }
    }

    async function createTodo(todo: TodoCreate): Promise<void> {
        try {
            await apiRequest(`${API_BASE_URL}/todos`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(todo),
            });
            await getTodos();
        } catch (e) {
            alert("Failed to create todo");
        }
    }

    async function fetchServer() {
        try {
            const data = await apiRequest<{status: string}>(`${API_BASE_URL}/health`);
            hello = data.status;
        } catch (e) {
            hello = "Backend Offline";
        }
    }

    function startPolling() {
        if (!isPollingActive) {
            isPollingActive = true;
            if (intervalId) clearInterval(intervalId);
            getTodos();
            intervalId = setInterval(getTodos, POLLING_INTERVAL);
            console.log('Polling started');
        }
    }

    function stopPolling() {
        if (isPollingActive) {
            isPollingActive = false;
            if (intervalId) {
                clearInterval(intervalId);
                intervalId = null;
                console.log('Polling stopped');
            }
        }
    }

    function togglePolling() {
        isPollingActive ? stopPolling() : startPolling();
    }

	onMount(() => {
        fetchServer();
        getTodos();
        startPolling();
        
        return () => {
            if (intervalId) clearInterval(intervalId);
        };
	});
</script>

<main class="p-10 space-y-4">
    <ModeWatcher />
    <h2 class="flex items-center gap-2 text-3xl font-bold">
        {#if hello === 'loading...'}
            <Spinner class="size-6" /> 
            <span>Backend is {hello}</span>
        {:else if hello === 'Backend Offline'}
            <Spinner class="size-6" /> 
            <span>{hello}</span>
        {:else}
            <span class="text-3xl font-bold">{hello}</span>
        {/if}
        <Button onclick={toggleMode} variant="outline" size="icon">
          <SunIcon
            class="h-[1.2rem] w-[1.2rem] scale-100 rotate-0 !transition-all dark:scale-0 dark:-rotate-90"
          />
          <MoonIcon
            class="absolute h-[1.2rem] w-[1.2rem] scale-0 rotate-90 !transition-all dark:scale-100 dark:rotate-0"
          />
          <span class="sr-only">Toggle theme</span>
        </Button>
    </h2>

	<h1 class="text-3xl font-bold">Todos:</h1>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        <AddTodoCard {createTodo} {togglePolling} />

        {#if todos.length > 0}
            {#each todos as todo (todo.todo_id)}
                <Card.Root class="w-full flex flex-col" size="sm">
                    <Card.Header>
                        {#if todo.editing}
                            <input 
                                bind:value={todo.todo_name} 
                                class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm mb-2" 
                                placeholder="Name"
                            />
                            <select 
                                bind:value={todo.todo_priority}
                                class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                            >
                                <option value={PriorityEnum.HIGH}>High</option>
                                <option value={PriorityEnum.MEDIUM}>Medium</option>
                                <option value={PriorityEnum.LOW}>Low</option>
                            </select>
                        {:else}
                            <Card.Title>{todo.todo_name}</Card.Title>
                            <Card.Description>Priority: {priorityLabels[todo.todo_priority] ?? todo.todo_priority}</Card.Description>
                        {/if}
                    </Card.Header>
                    
                    <Card.Content class="flex-grow">
                        {#if todo.editing}
                            <textarea 
                                bind:value={todo.todo_description} 
                                class="flex min-h-[60px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm" 
                                placeholder="Description"
                            ></textarea>
                        {:else}
                            <p class="whitespace-pre-wrap break-words text-sm text-gray-700">{todo.todo_description}</p>
                        {/if}
                    </Card.Content>
                    
                    <Card.Footer class="flex gap-2 pt-4 mt-auto">
                        {#if todo.editing}
                            <Button 
                                onclick={() => {
                                    updateTodo(todo.todo_id, {
                                        todo_name: todo.todo_name,
                                        todo_description: todo.todo_description,
                                        // Mapped to 'priority' for the API
                                        priority: Number(todo.todo_priority)
                                    });
                                    todo.editing = false;
                                    togglePolling();
                                }} 
                                variant="default" 
                                size="sm" 
                                class="flex-1 bg-green-600 hover:bg-green-700"
                            >
                                Confirm
                            </Button>
                        {:else}
                            <Button 
                                onclick={() => {todo.editing = true; stopPolling();}} 
                                variant="outline" 
                                size="sm" 
                                class="flex-1"
                            >
                                Edit
                            </Button>
                            <Button 
                                onclick={() => deleteTodo(todo.todo_id)} 
                                variant="destructive" 
                                size="sm" 
                                class="flex-1"
                            >
                                Remove
                            </Button>
                        {/if}
                    </Card.Footer>
                </Card.Root>
            {/each}
        {/if}
    </div>
</main>
