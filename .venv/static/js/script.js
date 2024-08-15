let userIds = [];
let currentIndex1 = 0;
let currentIndex2 = 1;

// Fetch the list of user IDs
function loadUserIds() {
    fetch('/user-ids')
        .then(response => response.json())
        .then(data => {
            userIds = data;
            loadUsers(currentIndex1, currentIndex2); // Load the first two users after IDs are loaded
        });
}

// Fetch and display user data by user ID
function loadUser(index, containerId) {
    if (index >= 0 && index < userIds.length) {
        const userId = userIds[index];
        fetch(`/user/${userId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById(containerId).innerHTML = `<p>Error loading user data</p>`;
                } else {
                    // Capitalize class name
                    const capitalizedClassName = data.className.charAt(0).toUpperCase() + data.className.slice(1);

                    document.getElementById(containerId).innerHTML = `
                        <img "https://crookedneighbor.github.io/habitica-avatar/avatar.html#${data.user_id}"
                        <h2>${data.username}</h2>
                        <p>Level ${data.level} ${capitalizedClassName}</p>
                        <p>${parseInt(data.gold, 10)} Gold</p>
                        <p>${parseInt(data.currHealth, 10)}/${data.maxHealth} Health</p>
                        <p>${parseInt(data.currExp, 10)}/${data.toNextLevelExp} Experience</p>
                        <p>Showing user ${index + 1} of ${userIds.length}</p>
                    `;
                }
            });
    }
}

// Load both users in containers
function loadUsers(index1, index2) {
    loadUser(index1, 'user-container-1');
    if (index2 < userIds.length) {
        loadUser(index2, 'user-container-2');
    } else {
        document.getElementById('user-container-2').innerHTML = `<p>No data available for comparison</p>`;
    }
}

// Event listeners for User 1 navigation
document.getElementById('prev-button-1').addEventListener('click', () => {
    if (currentIndex1 > 0) {
        currentIndex1--;
        if (currentIndex1 === currentIndex2) currentIndex1--;
        loadUsers(currentIndex1, currentIndex2);
    }
});

document.getElementById('next-button-1').addEventListener('click', () => {
    if (currentIndex1 < userIds.length - 1) {
        currentIndex1++;
        if (currentIndex1 === currentIndex2) currentIndex1++;
        loadUsers(currentIndex1, currentIndex2);
    }
});

// Event listeners for User 2 navigation
document.getElementById('prev-button-2').addEventListener('click', () => {
    if (currentIndex2 > 0) {
        currentIndex2--;
        if (currentIndex2 === currentIndex1) currentIndex2--;
        loadUsers(currentIndex1, currentIndex2);
    }
});

document.getElementById('next-button-2').addEventListener('click', () => {
    if (currentIndex2 < userIds.length - 1) {
        currentIndex2++;
        if (currentIndex2 === currentIndex1) currentIndex2++;
        loadUsers(currentIndex1, currentIndex2);
    }
});


// Load user IDs on page load
loadUserIds();
