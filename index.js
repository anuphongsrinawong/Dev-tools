window.addEventListener('scroll', function () {
    const sidebar = document.getElementById('sidebar');
    const tab = document.getElementById('tab');
    const headerHeight = 5; // ความสูงของ Header หรือ Navbar ด้านบน

    if (window.pageYOffset >= headerHeight) {
        sidebar.style.top = `${headerHeight}rem`;
        tab.style.top = `${headerHeight}rem`;
    } else {
        sidebar.style.top = '0';
        tab.style.top = '0';
    }
});




fetch('data.json')
    .then(response => response.json())
    .then(data => {
        // เลือก <ul> ที่มี id="sidebar-item"
        const sidebarItem = document.getElementById('sidebar-item');

        // สร้าง <li> สำหรับแต่ละรายการใน JSON
        data.forEach(menuItem => {
            const li = document.createElement('li');
            li.classList.add('nav-item');

            const button = document.createElement('button');
            button.classList.add('btn', 'btn-link', 'w-100');
            button.setAttribute('data-bs-toggle', 'collapse');
            button.setAttribute('data-bs-target', `#getStartedMenu${menuItem.id}`);
            button.setAttribute('aria-expanded', 'false');
            button.textContent = menuItem.title;

            const div = document.createElement('div');
            div.classList.add('collapse');
            div.id = `getStartedMenu${menuItem.id}`;

            const ul = document.createElement('ul');
            ul.classList.add('nav', 'flex-column', 'ms-3');

            // สร้างรายการเมนูย่อย
            menuItem.submenu.forEach(submenuItem => {
                const subLi = document.createElement('li');
                subLi.classList.add('nav-item');

                const a = document.createElement('a');
                a.classList.add('nav-link');
                a.href = submenuItem.link;
                a.textContent = submenuItem.title;

                subLi.appendChild(a);
                ul.appendChild(subLi);
            });

            // เพิ่ม element ลงไปใน DOM
            div.appendChild(ul);
            li.appendChild(button);
            li.appendChild(div);
            sidebarItem.appendChild(li);
        });
    })
    .catch(error => console.error('เกิดข้อผิดพลาดในการโหลด JSON:', error));