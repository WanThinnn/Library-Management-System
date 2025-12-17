/**
 * borrow_book.js - JavaScript for borrow book page
 * URLs are passed via data-* attributes on #borrow-config element
 */

// State variables
let selectedReaderId = null;
let selectedBooks = [];
let currentFilter = 'all';

// Get URLs from config element
function getConfig() {
    const config = document.getElementById('borrow-config');
    return {
        apiReadersUrl: config?.dataset.apiReadersUrl || '/api/readers/',
        apiBooksUrl: config?.dataset.apiBooksUrl || '/api/books/',
        apiBorrowingReadersUrl: config?.dataset.apiBorrowingReadersUrl || '/api/borrowing-readers/',
        borrowBookListUrl: config?.dataset.borrowBookListUrl || '/books/borrow/',
        borrowDateInputId: config?.dataset.borrowDateInputId || 'id_borrow_date'
    };
}

// ============ TAB FUNCTIONALITY ============

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        // Remove active from all tabs
        document.querySelectorAll('.tab-btn').forEach(b => {
            b.classList.remove('active', 'border-blue-600', 'text-blue-600');
            b.classList.add('border-transparent', 'text-gray-500');
        });

        // Add active to clicked tab
        this.classList.add('active', 'border-blue-600', 'text-blue-600');
        this.classList.remove('border-transparent', 'text-gray-500');

        // Hide all panes
        document.querySelectorAll('.tab-pane').forEach(p => p.classList.add('hidden'));

        // Show target pane
        const target = this.dataset.target;
        document.getElementById(target).classList.remove('hidden');

        // Load data if needed
        if (target === 'content-history') {
            loadBorrowHistory(currentFilter);
        }
    });
});

// ============ TAB 1: CHO MƯỢN ============

function loadReaders(search = '') {
    const config = getConfig();
    const url = new URL(config.apiReadersUrl, window.location.origin);
    if (search) url.searchParams.append('search', search);

    fetch(url)
        .then(response => response.ok ? response.json() : Promise.reject(response))
        .then(data => {
            const readerList = document.getElementById('readerList');
            if (!data.data?.length) {
                readerList.innerHTML = '<div class="text-center text-gray-500 py-4"><em>Không tìm thấy độc giả</em></div>';
            } else {
                readerList.innerHTML = data.data.map(reader => `
                    <div class="reader-item p-3 border-l-4 border-transparent cursor-pointer mb-2 rounded hover:bg-gray-50 dark:hover:bg-gray-700 hover:border-blue-500 transition-all ${reader.id === selectedReaderId ? 'bg-green-50 dark:bg-green-900 border-green-500 font-medium' : ''}" data-id="${reader.id}">
                        <div class="font-medium text-gray-900 dark:text-gray-100">${reader.name}</div>
                        <div class="text-sm text-gray-500 dark:text-gray-400">${reader.email}</div>
                    </div>
                `).join('');

                document.querySelectorAll('.reader-item').forEach(item => {
                    item.addEventListener('click', function () {
                        selectReader(this.dataset.id,
                            this.querySelector('.font-medium').textContent,
                            this.querySelector('.text-sm').textContent);
                    });
                });
            }
        })
        .catch(error => {
            document.getElementById('readerList').innerHTML = '<div class="text-red-500 py-4"><em>Lỗi tải danh sách</em></div>';
        });
}

function loadBooks(search = '') {
    const config = getConfig();
    const url = new URL(config.apiBooksUrl, window.location.origin);
    if (search) url.searchParams.append('search', search);

    fetch(url)
        .then(response => response.ok ? response.json() : Promise.reject(response))
        .then(data => {
            const bookList = document.getElementById('bookList');
            if (!data.data?.length) {
                bookList.innerHTML = '<div class="text-center text-gray-500 py-4"><em>Không tìm thấy sách</em></div>';
            } else {
                bookList.innerHTML = data.data.map(book => `
                    <div class="book-item p-3 border-l-4 border-transparent cursor-pointer mb-2 rounded hover:bg-gray-50 dark:hover:bg-gray-700 hover:border-blue-500 transition-all ${selectedBooks.includes(book.id) ? 'bg-green-50 dark:bg-green-900 border-green-500 font-medium' : ''}" data-id="${book.id}">
                        <div class="font-medium text-gray-900 dark:text-gray-100">${selectedBooks.includes(book.id) ? '' : ''}${book.title}</div>
                        <div class="text-sm text-gray-500 dark:text-gray-400">
                            ${book.year} • ${book.category}
                            <span class="bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 text-xs px-2 py-0.5 rounded-full ml-2">Còn ${book.remaining}</span>
                        </div>
                    </div>
                `).join('');

                document.querySelectorAll('.book-item').forEach(item => {
                    item.addEventListener('click', function () {
                        selectBook(this.dataset.id, this.querySelector('.font-medium').textContent);
                    });
                });
            }
        })
        .catch(error => {
            document.getElementById('bookList').innerHTML = '<div class="text-red-500 py-4"><em>Lỗi tải danh sách</em></div>';
        });
}

function selectReader(id, name, email) {
    selectedReaderId = id;
    document.getElementById('readerId').value = id;
    document.getElementById('selectedReader').innerHTML = `
        <div class="flex items-center justify-between">
            <div>
                <strong class="text-gray-900 dark:text-gray-100">${name}</strong><br>
                <small class="text-gray-500 dark:text-gray-400">${email}</small>
            </div>
            <button type="button" onclick="clearReader()" class="ml-2 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 font-bold text-lg leading-none" title="Xóa và chọn lại">
                ×
            </button>
        </div>
    `;

    // Update selectedReaderDisplay
    document.getElementById('readerSearch').value = email;
    document.getElementById('selectedReaderDisplay').classList.remove('hidden');
    document.getElementById('selectedReaderName').innerHTML = `
        <div class="flex items-center justify-between">
            <span class="text-gray-900 dark:text-gray-100">${name} (${email})</span>
            <button type="button" onclick="clearReader()" class="ml-2 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 font-bold text-lg leading-none" title="Xóa và chọn lại">
                ×
            </button>
        </div>
    `;
    
    // Hide reader list
    document.getElementById('readerList').innerHTML = '<div class="text-center text-gray-500 dark:text-gray-400 py-4"><em>Đã chọn độc giả</em></div>';

    checkFormValid();
}

function clearReader() {
    selectedReaderId = null;
    document.getElementById('readerId').value = '';
    document.getElementById('selectedReader').innerHTML = '<em class="text-gray-400">Chưa chọn</em>';
    document.getElementById('readerSearch').value = '';
    document.getElementById('selectedReaderDisplay').classList.add('hidden');
    loadReaders();
    checkFormValid();
}

function selectBook(id, title) {
    id = parseInt(id);

    if (selectedBooks.includes(id)) {
        selectedBooks = selectedBooks.filter(bookId => bookId !== id);
    } else {
        selectedBooks.push(id);
    }

    document.getElementById('bookId').value = selectedBooks.join(',');

    document.querySelectorAll('.book-item').forEach(item => {
        const itemId = parseInt(item.dataset.id);
        if (selectedBooks.includes(itemId)) {
            item.classList.add('bg-green-50', 'dark:bg-green-900', 'border-green-500', 'font-medium');
            item.classList.remove('border-transparent');
            item.querySelector('.font-medium').textContent = '' + item.querySelector('.font-medium').textContent.replace('', '');
        } else {
            item.classList.remove('bg-green-50', 'dark:bg-green-900', 'border-green-500', 'font-medium');
            item.classList.add('border-transparent');
            item.querySelector('.font-medium').textContent = item.querySelector('.font-medium').textContent.replace('', '');
        }
    });

    updateBookDisplay();
    checkFormValid();
}

function updateBookDisplay() {
    const selectedBookDiv = document.getElementById('selectedBook');
    if (selectedBooks.length === 0) {
        selectedBookDiv.innerHTML = '<em class="text-gray-400">Chưa chọn</em>';
    } else {
        const bookNames = [];
        selectedBooks.forEach(id => {
            const item = document.querySelector(`.book-item[data-id="${id}"]`);
            if (item) {
                bookNames.push(item.querySelector('.font-medium').textContent.replace('', ''));
            }
        });
        selectedBookDiv.innerHTML = `<strong class="text-gray-900 dark:text-gray-100">${bookNames.join(', ')}</strong><br><small class="text-gray-500 dark:text-gray-400">(${selectedBooks.length} quyển)</small>`;
    }
}

function checkFormValid() {
    const config = getConfig();
    const submitBtn = document.getElementById('submitBtn');
    const borrowDate = document.getElementById(config.borrowDateInputId);
    const hasDate = borrowDate?.value;
    const isValid = selectedReaderId && selectedBooks.length > 0 && hasDate;
    submitBtn.disabled = !isValid;
}

// ============ TAB 2: ĐỘC GIẢ ĐANG MƯỢN ============

function loadBorrowingReaders() {
    const config = getConfig();
    fetch(config.apiBorrowingReadersUrl)
        .then(response => response.ok ? response.json() : Promise.reject(response))
        .then(data => {
            const container = document.getElementById('borrowingReadersList');
            if (!data.data?.length) {
                container.innerHTML = '<div class="text-center text-gray-500 py-4"><em>Không có độc giả đang mượn sách</em></div>';
            } else {
                container.innerHTML = data.data.map(reader => `
                    <div class="borrowing-reader-item p-4 border-l-4 ${reader.is_overdue ? 'border-red-500 bg-red-50' : 'border-yellow-500 bg-yellow-50'} mb-3 rounded cursor-pointer hover:shadow-md transition-all" 
                         data-reader-id="${reader.reader_id}"
                         data-reader-name="${reader.reader_name}"
                         data-reader-email="${reader.reader_email}"
                         data-books='${JSON.stringify(reader.books)}'>
                        <div class="flex justify-between items-center">
                            <div>
                                <div class="font-semibold text-gray-900">${reader.reader_name}</div>
                                <div class="text-sm text-gray-500">${reader.reader_email}</div>
                            </div>
                            <div class="text-right">
                                <span class="inline-block px-2 py-1 text-xs rounded-full ${reader.is_overdue ? 'bg-red-500 text-white' : 'bg-blue-500 text-white'}">
                                    ${reader.is_overdue ? 'Quá hạn' : reader.borrowed_count + ' quyển'}
                                </span>
                                <div class="text-xs text-gray-500 mt-1">
                                    Phải trả: ${reader.latest_due_date}
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('');

                document.querySelectorAll('.borrowing-reader-item').forEach(item => {
                    item.addEventListener('click', function () {
                        const readerId = this.dataset.readerId;
                        const readerName = this.dataset.readerName;
                        const readerEmail = this.dataset.readerEmail;
                        const books = JSON.parse(this.dataset.books);
                        showBorrowingDetail(readerId, readerName, readerEmail, books);
                    });
                });
            }
        })
        .catch(error => {
            document.getElementById('borrowingReadersList').innerHTML = '<div class="text-red-500 py-4"><em>Lỗi tải danh sách</em></div>';
        });
}

function showBorrowingDetail(readerId, readerName, readerEmail, books) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    let booksHtml = books.map(book => {
        const [day, month, year] = book.due_date.split('/');
        const dueDate = new Date(year, month - 1, day);
        const isOverdue = dueDate < today;

        return `
            <tr class="${isOverdue ? 'bg-red-50' : ''}">
                <td class="px-4 py-2 text-sm"><strong>${book.title}</strong></td>
                <td class="px-4 py-2 text-sm whitespace-nowrap">${book.borrow_date}</td>
                <td class="px-4 py-2 text-sm whitespace-nowrap">${book.due_date}</td>
                <td class="px-4 py-2 text-sm whitespace-nowrap">
                    ${isOverdue ? '<span class="bg-red-500 text-white text-xs px-2 py-1 rounded-full">Quá hạn</span>' : '<span class="bg-green-500 text-white text-xs px-2 py-1 rounded-full">Còn hạn</span>'}
                </td>
            </tr>
        `;
    }).join('');

    const modalHtml = `
        <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" id="borrowingDetailModal">
            <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-hidden">
                <div class="bg-blue-600 text-white px-4 py-3 flex justify-between items-center">
                    <h5 class="font-semibold"> Chi tiết sách mượn</h5>
                    <button onclick="document.getElementById('borrowingDetailModal').remove()" class="text-white hover:text-gray-200">✕</button>
                </div>
                <div class="p-4 overflow-y-auto max-h-[70vh]">
                    <div class="grid grid-cols-2 gap-4 mb-4">
                        <div>
                            <h6 class="font-semibold text-gray-900 mb-2">Thông tin độc giả</h6>
                            <p class="text-sm text-gray-700"><strong>Tên:</strong> ${readerName}</p>
                            <p class="text-sm text-gray-700"><strong>Email:</strong> <a href="mailto:${readerEmail}" class="text-blue-600">${readerEmail}</a></p>
                        </div>
                        <div>
                            <h6 class="font-semibold text-gray-900 mb-2">Thống kê</h6>
                            <p class="text-sm text-gray-700"><strong>Tổng sách đang mượn:</strong> <span class="bg-blue-600 text-white text-xs px-2 py-1 rounded-full">${books.length} quyển</span></p>
                        </div>
                    </div>
                    <hr class="my-4">
                    <h6 class="font-semibold text-gray-900 mb-2">Danh sách sách mượn</h6>
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr><th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Tên sách</th><th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Ngày mượn</th><th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Phải trả</th><th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Trạng thái</th></tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">${booksHtml}</tbody>
                        </table>
                    </div>
                </div>
                <div class="bg-gray-50 px-4 py-3 flex justify-between">
                    <a href="/reader/${readerId}/" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">Xem chi tiết độc giả</a>
                    <button onclick="document.getElementById('borrowingDetailModal').remove()" class="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded-lg transition-colors">Đóng</button>
                </div>
            </div>
        </div>
    `;

    const oldModal = document.getElementById('borrowingDetailModal');
    if (oldModal) oldModal.remove();
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

// ============ TAB 3: LỊCH SỬ MƯỢN ============

function loadBorrowHistory(filter = 'all') {
    const config = getConfig();
    const historyList = document.getElementById('historyList');

    fetch(config.borrowBookListUrl + "?filter=" + filter)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const tableBody = doc.querySelector('tbody');

            if (tableBody && tableBody.innerHTML.trim()) {
                historyList.innerHTML = `
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-4 py-2 text-left text-xs font-semibold text-gray-600 whitespace-nowrap">Phiếu #</th>
                                    <th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Độc giả</th>
                                    <th class="px-4 py-2 text-left text-xs font-semibold text-gray-600 whitespace-nowrap">Ngày mượn</th>
                                    <th class="px-4 py-2 text-left text-xs font-semibold text-gray-600 whitespace-nowrap">Phải trả</th>
                                    <th class="px-4 py-2 text-left text-xs font-semibold text-gray-600 whitespace-nowrap">Ngày trả</th>
                                    <th class="px-4 py-2 text-left text-xs font-semibold text-gray-600 whitespace-nowrap">Trạng thái</th>
                                    <th class="px-4 py-2 text-left text-xs font-semibold text-gray-600 whitespace-nowrap">Hành động</th>
                                </tr>
                            </thead>
                            <tbody id="historyBody" class="divide-y divide-gray-200"></tbody>
                        </table>
                    </div>
                `;

                const rows = doc.querySelectorAll('tbody tr');
                let historyBody = document.getElementById('historyBody');
                rows.forEach(row => {
                    const clonedRow = row.cloneNode(true);
                    clonedRow.classList.add('hover:bg-gray-50');
                    historyBody.appendChild(clonedRow);
                });
            } else {
                historyList.innerHTML = '<div class="bg-blue-50 border-l-4 border-blue-500 text-blue-700 p-4 rounded">Không có dữ liệu</div>';
            }
        })
        .catch(error => {
            historyList.innerHTML = '<div class="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded">Lỗi tải dữ liệu</div>';
        });
}

// ============ EVENT LISTENERS ============

document.addEventListener('DOMContentLoaded', function () {
    const config = getConfig();

    // Tab 1
    document.getElementById('readerSearch')?.addEventListener('input', e => loadReaders(e.target.value));
    document.getElementById('bookSearch')?.addEventListener('input', e => loadBooks(e.target.value));
    document.getElementById(config.borrowDateInputId)?.addEventListener('change', checkFormValid);

    // Tab 3: Filter
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.filter-btn').forEach(b => {
                b.classList.remove('bg-blue-600', 'text-white', 'border-blue-600');
                b.classList.add('border-gray-300', 'text-gray-700');
            });
            this.classList.add('bg-blue-600', 'text-white', 'border-blue-600');
            this.classList.remove('border-gray-300', 'text-gray-700');
            currentFilter = this.dataset.filter;
            loadBorrowHistory(currentFilter);
        });
    });

    // Form submit loading
    document.getElementById('borrowForm')?.addEventListener('submit', function () {
        const btn = document.getElementById('submitBtn');
        const btnText = document.getElementById('submitBtnText');
        const btnLoading = document.getElementById('submitBtnLoading');

        if (btn && btnText && btnLoading) {
            btn.disabled = true;
            btnText.classList.add('hidden');
            btnLoading.classList.remove('hidden');
        }
    });

    // Initial load
    loadReaders();
    loadBooks();
    loadBorrowingReaders();
    setInterval(loadBorrowingReaders, 30000);
});
