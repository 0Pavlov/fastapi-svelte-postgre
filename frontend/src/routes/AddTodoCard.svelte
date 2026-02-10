<script lang="ts">
  import * as Card from "$lib/components/ui/card";
  import { Button } from "$lib/components/ui/button";
  import Plus from "@lucide/svelte/icons/plus";
  
  interface TodoCreate {
      todo_name: string;
      todo_description: string;
      todo_priority: number;
  }

  let { createTodo, togglePolling } = $props<{
      createTodo: (todo: TodoCreate) => Promise<void>;
      togglePolling: () => void;
  }>();
  
  let isExpanded = $state(false);
  let todoName = $state('');
  let todoDescription = $state('');
  let todoPriority = $state<number>(3); // Default Low

  function handleSubmit() {
    if (todoName.trim() && todoDescription.trim()) {
      createTodo({
          todo_name: todoName,
          todo_description: todoDescription,
          todo_priority: Number(todoPriority)
      });
      
      todoName = '';
      todoDescription = '';
      todoPriority = 3;
      isExpanded = false;
      togglePolling();
    }
  }
</script>

<Card.Root 
  class="w-full h-full overflow-hidden flex flex-col min-h-[200px] {!isExpanded ? 'p-0' : 'gap-2'}" 
  size="sm"
>
  {#if !isExpanded}
    <button 
      type="button"
      class="w-full h-full flex flex-col items-center justify-center cursor-pointer hover:bg-gray-50 transition-colors p-6 text-center"
      onclick={() => {isExpanded = true; togglePolling();}}
    >
      <div class="w-12 h-12 mb-3 rounded-full bg-blue-100 flex items-center justify-center">
        <Plus class="w-6 h-6 text-blue-600" />
      </div>
      <p class="text-gray-600 font-medium">Add New Todo</p>
      <p class="text-sm text-gray-400 mt-1">Click to create a new task</p>
    </button>
  {:else}
    <Card.Header>
      <Card.Title>Add New Todo</Card.Title>
    </Card.Header>
    
    <Card.Content class="flex-grow">
      <div class="space-y-3">
        <input
          type="text"
          placeholder="Todo Name"
          bind:value={todoName}
          class="w-full p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <textarea
          placeholder="Todo Description"
          bind:value={todoDescription}
          class="w-full p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          rows="3"
        ></textarea>
        
        <select
          bind:value={todoPriority}
          class="w-full p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value={1}>High</option>
          <option value={2}>Medium</option>
          <option value={3}>Low</option>
        </select>
      </div>
    </Card.Content>
    
    <Card.Footer class="flex gap-2 mt-auto">
      <Button 
        onclick={() => {isExpanded = false; togglePolling();}}
        type="button"
        variant="outline"
        size="sm"
        class="flex-1"
      >
        Cancel
      </Button>
      <Button 
        onclick={handleSubmit}
        variant="default"
        size="sm"
        class="flex-1"
        disabled={!todoName.trim() || !todoDescription.trim()}
      >
        Create
      </Button>
    </Card.Footer>
  {/if}
</Card.Root>
