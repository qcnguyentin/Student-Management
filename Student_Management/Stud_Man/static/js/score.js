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