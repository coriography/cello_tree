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
        allCellists = await res.json();
        displaycellists(allCellists.cellist_list);
    } catch (err) {
        console.error(err);
    }
};

const displaycellists = (cellists) => {
    const htmlString = cellists
        .map((cellist) => {
            return `
            <li class="cellist">
                <h2>${cellist.name}</h2>
                <p>id: ${cellist.id}</p>
            </li>
        `;
        })
        .join('');
    cellistsList.innerHTML = htmlString;
};

loadcellists();
