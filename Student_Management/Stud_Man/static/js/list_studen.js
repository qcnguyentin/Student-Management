function addToList(id, name, sex, dob, address, sdt, email) {
    fetch("/api/list-student", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "sex": sex,
            "dob": dob,
            "address": address,
            "sdt": sdt,
            "email": email
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => res.json()).then((data) => {
        let d = document.getElementsByClassName('list-counter')
        for (let i = 0; i < d.length; i++)
        d[i].innerHTML = data.size_of_class
    }) // js promise
}

function deleteList(student_id) {
    if (confirm("Bạn có chắc muốn xóa không") == true){
        fetch(`/api/list-student/${student_id}`, {
            method: "delete"
        }).then((res) => res.json()).then((data) => {
            let d = document.getElementsByClassName('list-counter')
            for (let i = 0; i < d.length; i++)
                d[i].innerHTML = data.size_of_class
            let a = document.getElementById(`student-list${student_id}`)
            a.style.display = 'none'
        }) // js promise
    };
}


function build() {
    if (confirm("Xác nhận lập danh sách?") == true) {
        fetch('/api/list-student').then(res => res.json()).then(data => {
                if (data.status === 200) {
                    location.reload()
                    alert("Thành công")
                }
                else
                {
                    alert("Thất bại")
                }
            })
    }
}

function changeClass() {
    let b = document.getElementById("btn-update-class")
    b.style.display = "block"
}