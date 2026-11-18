
const currentDate = document.getElementById("currentDate");

if (currentDate) {
    currentDate.textContent = new Intl.DateTimeFormat("es-DO", {
        dateStyle: "long"
    }).format(new Date());
}
