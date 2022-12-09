function spinner(status="block") {
    let s = document.getElementsByClassName("my-spinner")
    for (let i = 0; i < s.length; i++)
        s[i].style.display = status
}

function addToScore(student_name, type_score, score) {
    fetch("/api/score", {
        method: "post",
        body: JSON.stringify({
            "student_name": student_name,
            "type_score": type_score,
            "score": score
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
}

function checkValue() {
    let a = document.getElementsByClassName("1")
    for (let i = 0; i < a.length; i++)
        console.info(a[i].value)
}