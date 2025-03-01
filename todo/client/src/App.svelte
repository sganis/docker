<script>
    import { onMount } from "svelte";
    let todos = $state([]);
    let newTodo = $state("");

    async function fetchTodos() {
        const response = await fetch("/api/todos");
        todos = await response.json();
    }

    async function addTodo() {
        if (newTodo.trim() === "") return;
        const response = await fetch("/api/todos", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: newTodo, completed: false })
        });
        const data = await response.json();
        todos = [...todos, data];
        newTodo = "";
    }

    async function toggleComplete(todo) {
      // console.log("Before:", JSON.parse(JSON.stringify(todo)));
      // const updatedTodo = { ...todo, completed: !todo.completed };
      // console.log("After:", JSON.parse(JSON.stringify(updatedTodo)));
      
      try{
        const response = await fetch(`/api/todos/${todo.id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(todo)
        })
        const data = await response.json();
        console.log(data);
      } catch (error) {
        console.error(error);
      }
      fetchTodos();
  }


    async function deleteTodo(id) {
        await fetch(`/api/todos/${id}`, { method: "DELETE" });
        fetchTodos();
    }

    onMount(fetchTodos);
</script>

<main>
    <h1>Todo App</h1>
    <input type="text" bind:value={newTodo} placeholder="New Todo" />
    <button onclick={addTodo}>Add</button>
    <ul>
        {#each todos as todo}
            <li>
              <input type="checkbox" bind:checked={todo.completed} 
                onchange={() => toggleComplete(todo)} />
                {todo.title}
                <button onclick={() => deleteTodo(todo.id)}>❌</button>
            </li>
        {/each}
    </ul>
</main>