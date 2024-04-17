const fpwrange = document.getElementById("fpwrange");
const fpwval = document.getElementById("fpwval");

const swrange = document.getElementById("swrange");
const swval = document.getElementById("swval");

const dwrange = document.getElementById("dwrange");
const dwval = document.getElementById("dwval");

const cwrange = document.getElementById("cwrange");
const cwval = document.getElementById("cwval");

const ywrange = document.getElementById("ywrange");
const ywval = document.getElementById("ywval");

const gwrange = document.getElementById("gwrange");
const gwval = document.getElementById("gwval");

fpwrange.addEventListener("input", () => {
    fpwval.innerHTML = fpwrange.value;
});

swrange.addEventListener("input", () => {
    swval.innerHTML = swrange.value;
});

dwrange.addEventListener("input", () => {
    dwval.innerHTML = dwrange.value;
});

cwrange.addEventListener("input", () => {
    cwval.innerHTML = cwrange.value;
});

ywrange.addEventListener("input", () => {
    ywval.innerHTML = ywrange.value;
});

gwrange.addEventListener("input", () => {
    gwval.innerHTML = gwrange.value;
});