function getusers() {
    const url = "http://localhost:5000/users"
    fetch(url)
    .then(response => response.json())
    .then(data =>{
        const usertable = document.getElementById("Userlist").getElementsByTagName("tbody")[0];
        data.forEach(element => {
            const row = usertable.insertRow(usertable.rows.length)
            const cell1 = row.insertCell(0);
            const cell2 = row.insertCell(1);
            const cell3 = row.insertCell(2);
            cell1.innerHTML=element;
            const button = document.createElement("button");

            
            button.innerText = "Send Email";
            button.id = "myButton";  
            button.className = "my-button-class";  

            button.addEventListener("click", function() {
                sendEmail(element);
                button.disabled = true;
            });
            
            cell2.append(button)

            const button2 = document.createElement("button");
            button2.innerText = "Show History";

            button2.addEventListener("click", function(){
                getHistory(element);
            });
            cell3.append(button2)
        });
    })
    .catch(error =>{console.error(error);});
}


function sendEmail(emailId){
    const email ={
        email: emailId
    }
    const url = "http://localhost:5000/sendEmail";
    fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(email)
    })
    .then(response =>{
        if(response.ok){
            console.log("email sent");
        }else{
            console.log("request failed");
        }
    })
    .catch(error=>{
        console.error("Error:", error);
    });
}

function getHistory(emailId) {
    console.log("emailId:"+emailId);
    const url = `http://localhost:5000/getEmailHistory?email=${emailId}`;
    
    fetch(url)
    .then(response => {
        if (response.ok) {
            
            return response.json();
        } else {
            throw new Error("Request failed");
        }
    })
    .then(data =>{
        let table = document.getElementById("dataTable");
        if (!table) {
            table = document.createElement("table");
            table.id = "dataTable";

            // Create the table header
            const thead = document.createElement("thead");
            const headerRow = thead.insertRow();
            const header1 = document.createElement("th");
            header1.textContent = "ID";
            const header2 = document.createElement("th");
            header2.textContent = "Time";
            const header3 = document.createElement("th");
            header3.textContent = "Receiver";

            headerRow.appendChild(header1);
            headerRow.appendChild(header2);
            headerRow.appendChild(header3);

            const tbody = document.createElement("tbody");

            table.appendChild(thead);
            table.appendChild(tbody);

            document.body.appendChild(table);
        }

        const tbody = table.getElementsByTagName("tbody")[0];
        tbody.innerHTML = "";
        data.history.forEach(item => {
            const row = tbody.insertRow(tbody.rows.length);
            const cell1 = row.insertCell(0);
            const cell2 = row.insertCell(1);
            const cell3 = row.insertCell(2);

            cell1.innerHTML = item.id;
            cell2.innerHTML = item.time;
            cell3.innerHTML = item.receiver;
        });
     })
    .catch(error =>{
        console.error("error:", error);
    });
}