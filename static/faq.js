function toggleAnswer(element) {
    element.classList.toggle("active");
    const answer = element.nextElementSibling;
    answer.style.display = answer.style.display === "block" ? "none" : "block";
}
