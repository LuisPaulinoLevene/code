const API =
    window.location.hostname === "localhost"
        ? "http://localhost:8000"
        : "/api";

let usuario=null;


// ================= MENSAGEM =================

function mensagem(texto){

let box=document.getElementById("msg");

if(box)

box.innerHTML=`
<div class="message">
${texto}
</div>`;

}



// ================= MODAIS =================

function abrirCadastro(){

fecharModais();

document
.getElementById("modalCadastro")
?.classList.remove("hidden");

}



function abrirLogin(){

fecharModais();

document
.getElementById("modalLogin")
?.classList.remove("hidden");

}



function abrirDeposito(){

fecharModais();

document
.getElementById("modalDeposito")
?.classList.remove("hidden");

}



function fecharModais(){

[
"modalCadastro",
"modalLogin",
"modalDeposito"
].forEach(id=>{

document
.getElementById(id)
?.classList.add("hidden");

});

}



// ================= SUPORTE =================


function abrirSuporte(){

document
.getElementById("modalSuporte")
?.classList.remove("hidden");

}



function fecharSuporte(){

document
.getElementById("modalSuporte")
?.classList.add("hidden");

}



// ================= CADASTRO =================


async function cadastrar(){

let dados={

email:cadEmail.value,

senha:cadSenha.value

};


try{


let resposta=await fetch(
`${API}/usuarios/`,
{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify(dados)

});


let retorno=await resposta.json();


if(resposta.ok){

mensagem(
"Cadastro realizado. Faça login."
);

fecharModais();

}

else{

mensagem(
retorno.detail || "Erro no cadastro"
);

}


}catch(e){

mensagem(
"Servidor indisponível"
);

}


}



// ================= LOGIN =================


async function login(){


let dados={

email:logEmail.value,

senha:logSenha.value

};


try{


let resposta=await fetch(
`${API}/usuarios/login`,
{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify(dados)

});


let retorno=await resposta.json();



if(!resposta.ok){

mensagem(
retorno.detail ||
"Erro no login"
);

return;

}



usuario=retorno;


localStorage.setItem(
"usuario_id",
usuario.id
);



mostrarMenuUsuario();


mensagem(
"Login efetuado com sucesso"
);


fecharModais();



}catch(e){

mensagem(
"Erro de ligação ao servidor"
);

}


}





// ================= MENU USUARIO =================


function mostrarMenuUsuario(){


menuLogin.classList.add("hidden");


menuUsuario.classList.remove("hidden");



emailTopo.innerHTML=
"👤 "+usuario.email;



buscarSaldo();


}



// ================= SAIR =================


function sair(){

localStorage.removeItem(
"usuario_id"
);


location.reload();

}



// ================= SALDO =================


async function buscarSaldo(){


let id=
localStorage.getItem("usuario_id");


if(!id)return;



try{


let resposta=await fetch(
`${API}/calcular/saldo/${id}`
);



let dados=await resposta.json();



if(resposta.ok){


let saldo=document.getElementById(
"saldoTopo"
);


if(saldo)

saldo.innerHTML=dados.saldo;


}



}catch(e){

console.log(e);

}


}





// ================= MARCAS =================


async function carregarMarcas(){


try{


let resposta=await fetch(
`${API}/calcular/marcas`
);



let marcas=await resposta.json();



let select=document.getElementById(
"marca"
);



select.innerHTML=`

<option value="">
Selecione marca
</option>

`;



marcas.forEach(m=>{


select.innerHTML+=`

<option value="${m.id}">
${m.marca}
</option>

`;


});



}catch(e){


mensagem(
"Erro ao carregar marcas"
);


}


}





// ================= MODELOS =================


document
.getElementById("marca")
.addEventListener(
"change",
async function(){


let id=this.value;


if(!id)return;



try{


let resposta=await fetch(
`${API}/calcular/modelos/${id}`
);



let modelos=await resposta.json();



modelo.innerHTML=`

<option value="">
Selecione modelo
</option>

`;



modelos.forEach(m=>{


modelo.innerHTML+=`

<option value="${m.id}">
${m.modelo}
</option>

`;


});



}catch(e){

mensagem(
"Erro ao carregar modelos"
);

}


});







// ================= CALCULAR =================


async function calcular(){


let id=
localStorage.getItem("usuario_id");



if(!id){

mensagem(
"Faça login primeiro."
);

return;

}




let dados={

usuario_id:Number(id),

imei:
imei.value.trim(),

marca_id:Number(
marca.value
),

modelo_id:Number(
modelo.value
)

};




if(dados.imei.length!==15){

mensagem(
"IMEI deve ter 15 números."
);

return;

}



try{


let resposta=await fetch(
`${API}/calcular/`,
{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:
JSON.stringify(dados)

});



let retorno=await resposta.json();



if(resposta.ok){


resultado.innerHTML=`

<div class="codigo-final">

${retorno.codigo}

</div>

`;



buscarSaldo();


}

else{


mensagem(
retorno.detail ||
"Erro ao calcular"
);


}



}catch(e){


mensagem(
"Erro no servidor"
);


}



}





// ================= DEPOSITO =================


async function recarregar(){



let id=
localStorage.getItem("usuario_id");



if(!id){

mensagem(
"Faça login primeiro."
);

return;

}




let dados={


usuario_id:Number(id),


valor:Number(
valor.value
),


numero:
numero.value,


metodo:
metodo.value


};




if(!dados.valor){

mensagem(
"Digite o valor."
);

return;

}



try{


let resposta=await fetch(
`${API}/calcular/recarga`,
{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:
JSON.stringify(dados)

});



let retorno=await resposta.json();



if(resposta.ok){


mensagem(
"Depósito confirmado."
);



buscarSaldo();


fecharModais();


}

else{


mensagem(
retorno.detail ||
"Erro no depósito"
);


}



}catch(e){


mensagem(
"Erro de ligação."
);


}



}







// ================= RECUPERAR LOGIN =================


async function verificarLogin(){


let id=
localStorage.getItem("usuario_id");



if(!id)return;



try{


let resposta=await fetch(
`${API}/usuarios/${id}`
);



if(resposta.ok){


usuario=
await resposta.json();



mostrarMenuUsuario();


}



}catch(e){

console.log(e);

}


}







// ================= ANO =================


let ano=document.getElementById("ano");


if(ano)

ano.innerHTML=
new Date().getFullYear();







// ================= INICIO =================


carregarMarcas();

verificarLogin();