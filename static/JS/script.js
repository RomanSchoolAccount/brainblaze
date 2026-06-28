const slidesData = [
  {
    image: "../static/Img/CTA1.svg",
    title: "Performance Mental",
    text: "Leva o teu foco ao limite com os nossos nootrópicos avançados e domina qualquer partida.",
    buttonLink: "/Produtos",
    buttonText: "Explorar Foco"
  },
  {
    image: "../static/Img/CTA2.jpg",
    title: "Energia Máxima",
    text: "Sem quebras de energia. Mantém-te ativo nas sessões mais longas e exigentes.",
    buttonLink: "/Produtos",
    buttonText: "Ver Bebidas"
  },
  {
    image: "../static/Img/CTA3.jpg",
    title: "Alta Produtividade",
    text: "Potencia o teu fluxo de trabalho. Desbloqueia o verdadeiro potencial do teu cérebro.",
    buttonLink: "/Produtos",
    buttonText: "Comprar Agora"
  },
  {
    image: "../static/Img/CTA4.jpg",
    title: "Sobre a BrainBlaze",
    text: "Conhece a história por trás da marca que está a revolucionar a tua rotina.",
    buttonLink: "/SobreNos",
    buttonText: "Saber Mais"
  }
];

let current = 0;

const cta = document.getElementById("cta");
const radios = document.querySelectorAll(".Balls input");

const ctaTitle = document.getElementById("cta-title");
const ctaText = document.getElementById("cta-text");
const ctaBtn = document.getElementById("cta-btn");

function updateSlide(index) {
  current = index;
  const currentSlide = slidesData[current];

  cta.style.backgroundImage = `url(${currentSlide.image})`;
  radios[current].checked = true;

  ctaTitle.textContent = currentSlide.title;
  ctaText.textContent = currentSlide.text;
  ctaBtn.href = currentSlide.buttonLink;
  ctaBtn.textContent = currentSlide.buttonText;
}

document.getElementById("next").onclick = () => {
  updateSlide((current + 1) % slidesData.length);
};

document.getElementById("prev").onclick = () => {
  updateSlide((current - 1 + slidesData.length) % slidesData.length);
};

radios.forEach(radio => {
  radio.addEventListener("change", (e) => {
    updateSlide(parseInt(e.target.dataset.index));
  });
});

updateSlide(0);




document.getElementById("newsletter-form").addEventListener("submit", function(e) {
  e.preventDefault();
  

  const email = document.getElementById("email").value;

  fetch("https://yourapi.com/newsletter", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email })
  })
  .then(() => alert("Subscrito com sucesso!"))
  .catch(() => alert("Erro ao enviar"));
});

document.addEventListener("DOMContentLoaded", function() {

    const filtrosCategoria = document.querySelectorAll('input[name="filtro-categoria"]');
    const filtrosDesconto = document.querySelectorAll('input[name="filtro-desconto"]');
    const filtrosPreco = document.querySelectorAll('input[name="filtro-preco"]');
    const cards = document.querySelectorAll('.product-showcase-card');

    function filtrar() {

        const catsMarcadas = Array.from(filtrosCategoria).filter(i => i.checked).map(i => i.value.toString());
        const descsMarcadas = Array.from(filtrosDesconto).filter(i => i.checked);
        const precosMarcados = Array.from(filtrosPreco).filter(i => i.checked);

        const mostrarTudoCat = catsMarcadas.length === 0 || catsMarcadas.length === filtrosCategoria.length;
        const mostrarTudoDesc = descsMarcadas.length === 0 || descsMarcadas.length === filtrosDesconto.length;
        const mostrarTudoPreco = precosMarcados.length === 0 || precosMarcados.length === filtrosPreco.length;

        cards.forEach(card => {
            const catProd = card.getAttribute('data-categoria');
            const precoOrig = parseFloat(card.getAttribute('data-preco'));
            const descProd = parseInt(card.getAttribute('data-desconto')) || 0;
            const precoFinal = descProd > 0 ? precoOrig * (1 - (descProd / 100)) : precoOrig;

            let okCat = mostrarTudoCat || catsMarcadas.includes(catProd);

            let okDesc = mostrarTudoDesc;
            if (!mostrarTudoDesc) {
                descsMarcadas.forEach(cb => {
                    const texto = cb.parentElement.textContent.toLowerCase();
                    if (texto.includes("até 20%") && descProd > 0 && descProd <= 20) okDesc = true;
                    if (texto.includes("20% a 30%") && descProd > 20 && descProd <= 30) okDesc = true;
                    if (texto.includes("30% a 50%") && descProd > 30 && descProd <= 50) okDesc = true;
                    if (texto.includes("superior a 50%") && descProd > 50) okDesc = true;
                });
            }

            let okPreco = mostrarTudoPreco;
            if (!mostrarTudoPreco) {
                precosMarcados.forEach(cb => {
                    const texto = cb.parentElement.textContent.toLowerCase();
                    if (texto.includes("0 - €30") && precoFinal <= 30) okPreco = true;
                    if (texto.includes("30 - €150") && precoFinal > 30 && precoFinal <= 150) okPreco = true;
                    if (texto.includes("150 - €300") && precoFinal > 150 && precoFinal <= 300) okPreco = true;
                    if (texto.includes("300 - €400") && precoFinal > 300 && precoFinal <= 400) okPreco = true;
                    if (texto.includes("400 - €500") && precoFinal > 400 && precoFinal <= 500) okPreco = true;
                    if (texto.includes("mais de €500") && precoFinal > 500) okPreco = true;
                });
            }

            if (okCat && okDesc && okPreco) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    }

    const todosInputs = document.querySelectorAll('.products-sidebar input[type="checkbox"]');
    todosInputs.forEach(input => {
        input.addEventListener('change', filtrar);
    });

    filtrar();
});

document.getElementById('newsletter-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const emailInput = document.getElementById('newsletter-email');
    const emailValue = emailInput.value;

    fetch('/Newsletter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: emailValue })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            emailInput.value = ''; 
        } else {
            alert('Ocorreu um erro: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Não foi possível enviar o email de momento.');
    });
});