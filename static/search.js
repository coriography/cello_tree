const cellistsList = document.getElementById('cellistsList');
const searchBar = document.getElementById('searchBar');
let allCellists = [];

searchBar.addEventListener('keyup', (e) => {
    const searchString = e.target.value.toLowerCase();

    const filteredcellists = allCellists.filter((cellist) => {
        return (
            cellist.name.toLowerCase().includes(searchString)
        );
    });
    displaycellists(filteredcellists);
});

const loadcellists = async () => {
    try {
        const res = await fetch('/api/all_cellists');
        const json = await res.json();
        allCellists = json.cellist_list;
        displaycellists(allCellists);
    } catch (err) {
        console.error(err);
    }
};

const displaycellists = (cellists) => {
    const htmlString = cellists
        .map((cellist) => {
            const img_url = cellist.img_url ? cellist.img_url : '/static/img/cello_1.jpg';
            return `
            <div class="col-12 col-md-6 col-lg-4 d-flex">
            <div class="card cellist-card box-shadow-sm">
                <div class="row no-gutters h-100">
                    <div class="col-4">
                        <div class="cellist-card-img w-100 h-100" style="background-image: url('${img_url}')"></div>
                    </div>
                    <div class="col-8">
                        <div class="card-body h-100">
                            <h5 class="card-title text-black">${cellist.name}</h5>
                            <div class="row">
                                <div class="col-4 pr-0">
                                    <p class="card-text">${cellist.num_teachers} <br><small class="text-muted">teachers</small></p>
                                </div>
                                <div class="col-4 pr-0">
                                    <p class="card-text">${cellist.num_students} <br><small class="text-muted">students</small></p>
                                </div>
                                <div class="col-4">
                                    <p class="card-text">${cellist.num_posts} <br><small class="text-muted">posts</small></p>
                                </div>
                            </div>
                            <a href="/cellist_profile/${cellist.id}" class="btn btn-secondary mt-3 mx-0">View profile</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;
        })
        .join('');
    cellistsList.innerHTML = htmlString;
};

loadcellists();
