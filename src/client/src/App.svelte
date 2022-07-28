<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3'  

  let vis; // binding with div for visualization
  let authors;

  function addRequestHeaders(headersDict) {
    return Object.assign(headersDict, { "credentials":"include", 
                                        "referrerPolicy":"no-referrer-when-downgrade",
                                        "mode":"no-cors"})
    }
  


  onMount(async () => {
    fetch("http://127.0.0.1:5002/get_authors/")
    .then(response => response.json())
    .then(data => { 
		  console.log(data);
      authors = data;
    }).catch(error => {
      console.log(error);
      return [];
    });
})

  function drawVis() { 
    d3.select(vis).html();
    const width = 1200,
          height = 800;
    
    
    
    




  }


</script>

<main>
  <h1>Svelte + D3</h1> 

  <div id="vis" bind:this={vis}></div>
  
</main>

<style>

</style>
