function addStudent(){
    fetch('/api/student/add-student', {
        method: "post",
        body: JSON.stringify({
            'student_name': document.getElementById("add-student-name").value,
            'student_sex': document.getElementById("add-student-sex").value,
            'student_dob': document.getElementById("add-student-dob").value,
            'student_address': document.getElementById("add-student-address").value,
            'student_phone': document.getElementById("add-student-phone").value,
            'student_email': document.getElementById("add-student-email").value,
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => res.json()).then((data) => {
       alert(data.error)
    }) // js promise
}

function updateStudent(){
    fetch('/api/student/add-student', {
        method: "update",
        body: JSON.stringify({
            'student_id': document.getElementById("update-student-id").value,
            'student_name': document.getElementById("update-student-name").value,
            'student_sex': document.getElementById("update-student-sex").value,
            'student_dob': document.getElementById("update-student-dob").value,
            'student_address': document.getElementById("update-student-address").value,
            'student_phone': document.getElementById("update-student-phone").value,
            'student_email': document.getElementById("update-student-email").value,
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => res.json()).then((data) => {
       alert(data.error)
    }) // js promise
}

function loadScoresDetail() {
    fetch(`/api/student/add-student`)
}