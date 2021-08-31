const searchBlock = document.querySelector('#searchBlock');

const pagination = document.querySelector(".pagination");

const colAfterAjax = document.querySelector(".col-after-ajax");
const colBeforeAjax = document.querySelector(".col-before-ajax");
colAfterAjax .style.display = "none";


searchBlock.addEventListener("keyup", (e) => {
    const  searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        pagination.style.display = 'none';
        colAfterAjax.innerHTML = '';


        fetch("news/search", {
            body: JSON.stringify({searchQuery: searchValue}),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {

                colBeforeAjax.style.display = "none";
                colAfterAjax.style.display = "block";

                if (data.length === 0) {
                    colAfterAjax.innerHTML = "Ничего не найдено.";
                }else {
                    data.forEach((item) =>{
                        colAfterAjax.innerHTML +=`                            
                             <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm position-relative  bg-white ">
                        <div class="col p-4 d-flex flex-column position-static">
                            <br>
                            <h3 class="mb-3 mt-3">${item.title}</h3>
                            <p class="card-text mb-auto mt-3">${item.description}</p>
                            <a href="/blog/news/${item.id}" class="text-muted">Подробнее</a>
                        </div>
                    </div>
                            `;
                    });
                }
            });

    }else {
        colAfterAjax.style.display = "none";
        colBeforeAjax.style.display = "block";
        pagination.style.display = 'block';
    }
})