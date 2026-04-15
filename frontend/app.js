let history = [];

async function ask(){
  const input=document.getElementById("q");
  const chat=document.getElementById("chat");
  const ctx=document.getElementById("context");

  let q=input.value.trim();
  if(!q)return;

  append(q,"user");
  input.value="";

  let typing=append("Thinking...","bot");

  try{
    const res=await fetch("http://localhost:8000/ask",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({question:q,history})
    });

    const data=await res.json();
    history=data.history;

    typing.remove();
    append(data.answer,"bot");

    ctx.innerHTML="";
    if(data.context){
      data.context.forEach(c=>{
        let div=document.createElement("div");
        div.className="context-box";
        div.innerHTML=marked.parse(c);
        ctx.appendChild(div);
      });
    }

  }catch(e){
    typing.remove();
    append("Error connecting backend","bot");
  }
}

function append(text,type){
  const chat=document.getElementById("chat");
  let div=document.createElement("div");
  div.className="msg "+type;
  div.innerHTML=marked.parse(text);
  chat.appendChild(div);
  chat.scrollTop=chat.scrollHeight;
  return div;
}

document.getElementById("q").addEventListener("keypress",e=>{
 if(e.key==="Enter")ask();
});
