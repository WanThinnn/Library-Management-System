/**
 * return_book.js - JavaScript for return book page
 * URLs and data are passed via data-* attributes on #return-config element
 */

// State variables - will be initialized from config
let readersData = [];
let paramsData = {};
let selectedReader = null;
let selectedBooks = [];
let currentFilter = 'all';

// Get config from element
function getConfig() {
    const config = document.getElementById('return-config');
    return {
        returnBookListUrl: config?.dataset.returnBookListUrl || '/books/return/',
        returnDateInputId: config?.dataset.returnDateInputId || 'id_return_date',
        borrowedBooksApiUrl: config?.dataset.borrowedBooksApiUrl || '/api/reader/{readerId}/borrowed-books/'
    };
}

// Initialize data from config
function initData() {
    const config = document.getElementById('return-config');
    try {
        readersData = JSON.parse(config?.dataset.readersJson || '[]');
        paramsData = JSON.parse(config?.dataset.paramsJson || '{}');
    } catch (e) {
        console.error('Error parsing config data:', e);
    }
}

// ============ TAB FUNCTIONALITY ============

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        document.querySelectorAll('.tab-btn').forEach(b => {
            b.classList.remove('active', 'border-blue-600', 'text-blue-600');
            b.classList.add('border-transparent', 'text-gray-500');
        });

        this.classList.add('active', 'border-blue-600', 'text-blue-600');
        this.classList.remove('border-transparent', 'text-gray-500');

        document.querySelectorAll('.tab-pane').forEach(p => p.classList.add('hidden'));

        const target = this.dataset.target;
        document.getElementById(target).classList.remove('hidden');

        if (target === 'content-history') {
            loadReturnHistory(currentFilter);
        }
    });
});

// Initialize
document.addEventListener('DOMContentLoaded', function () {
    const config = getConfig();
    initData();

    loadReaders();

    document.getElementById('readerSearch')?.addEventListener('input', function () {
        filterReaders(this.value.toLowerCase());
    });

    document.getElementById(config.returnDateInputId)?.addEventListener('change', function () {
        updateSubmitButton();
    });

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.filter-btn').forEach(b => {
                b.classList.remove('bg-blue-600', 'text-white', 'border-blue-600');
                b.classList.add('border-gray-300', 'text-gray-700');
            });
            this.classList.add('bg-blue-600', 'text-white', 'border-blue-600');
            this.classList.remove('border-gray-300', 'text-gray-700');
            currentFilter = this.dataset.filter;
            loadReturnHistory(currentFilter);
        });
    });

    // Form submit loading
    document.getElementById('returnForm')?.addEventListener('submit', function () {
        const btn = document.getElementById('submitBtn');
        const btnText = document.getElementById('submitBtnText');
        const btnLoading = document.getElementById('submitBtnLoading');

        if (btn && btnText && btnLoading) {
            btn.disabled = true;
            btnText.classList.add('hidden');
            btnLoading.classList.remove('hidden');
        }
    });

    loadReturnHistory();
});

function loadReaders() {
    const readerList = document.getElementById('readerList');
    if (!readersData.length) {
        readerList.innerHTML = '<div class="text-center text-gray-500 p-3"><small>Không có độc giả</small></div>';
        return;
    }

    renderReadersList(readersData.slice(0, 5));
}

function renderReadersList(readers) {
    const readerList = document.getElementById('readerList');
    if (!readers.length) {
        readerList.innerHTML = '<div class="text-center text-gray-500 p-3"><small>Không tìm thấy độc giả</small></div>';
        return;
    }

    readerList.innerHTML = readers.map(reader => `
        <div class="reader-item p-3 border-b border-gray-200 cursor-pointer hover:bg-gray-100 transition-all" data-reader-id="${reader.id}">
            <div class="font-medium text-gray-900">${reader.reader_name}</div>
            <div class="text-sm text-gray-500">${reader.email}</div>
        </div>
    `).join('');

    document.querySelectorAll('.reader-item').forEach(item => {
        item.addEventListener('click', function () {
            selectReader(parseInt(this.dataset.readerId));
        });
    });
}

function filterReaders(query) {
    if (!query) {
        renderReadersList(readersData.slice(0, 5));
        return;
    }

    const filtered = readersData.filter(r =>
        r.reader_name.toLowerCase().includes(query) ||
        r.email.toLowerCase().includes(query)
    ).slice(0, 5);

    renderReadersList(filtered);
}

function selectReader(readerId) {
    selectedReader = readerId;
    selectedBooks = [];

    const reader = readersData.find(r => r.id === readerId);

    document.getElementById('readerSearch').value = '';
    document.getElementById('selectedReaderDisplay').classList.remove('hidden');
    document.getElementById('selectedReaderName').textContent = reader.reader_name + ' (' + reader.email + ')';

    // Update form panel reader display
    const readerDisplay2 = document.getElementById('selectedReaderDisplay2');
    if (readerDisplay2) {
        readerDisplay2.innerHTML = `<strong>${reader.reader_name}</strong>`;
    }

    document.getElementById('readerList').innerHTML = `
        <div class="text-center text-gray-500 p-2">
            <small>Độc giả đã chọn: <strong>${reader.reader_name}</strong></small>
        </div>
    `;

    // Reset books display in form panel
    const booksDisplay = document.getElementById('selectedBooksDisplay');
    if (booksDisplay) {
        booksDisplay.innerHTML = '<em class="text-gray-400">Chưa chọn</em>';
    }

    loadReaderBooks(selectedReader);
    updateSummary();
}

function loadReaderBooks(readerId) {
    const config = getConfig();
    let url = config.borrowedBooksApiUrl.replace('{readerId}', readerId);

    fetch(url, {
        credentials: 'same-origin'
    })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            renderBooks(data.data || []);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('booksList').innerHTML = `<div class="bg-red-50 border-l-4 border-red-500 text-red-700 p-3 rounded">Lỗi tải danh sách: ${error.message}</div>`;
        });
}

function renderBooks(books) {
    const booksList = document.getElementById('booksList');

    if (!books.length) {
        booksList.innerHTML = '<div class="text-center text-gray-500"><em>Độc giả này không có sách mượn chưa trả</em></div>';
        return;
    }

    booksList.innerHTML = books.map((book, idx) => `
        <div class="book-item p-3 border border-gray-200 rounded-lg mb-2 flex items-center gap-3 cursor-pointer hover:bg-gray-50 transition-all ${book.is_overdue ? 'bg-yellow-50 border-yellow-400' : 'bg-gray-50'}" data-book-id="${book.book_item_id}">
            <input type="checkbox" class="book-checkbox w-5 h-5 cursor-pointer" value="${book.book_item_id}" onchange="updateSelectedBooks()">
            <div class="flex-1">
                <div class="font-medium text-gray-900">${book.book_title}</div>
                <div class="text-sm text-gray-500">
                    Mượn: ${book.borrow_date} | Phải trả: ${book.due_date}
                    ${book.is_overdue ? `<span class="bg-yellow-400 text-gray-900 text-xs px-2 py-0.5 rounded-full ml-2">Quá hạn ${book.days_overdue} ngày</span>` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

function updateSelectedBooks() {
    const config = getConfig();
    selectedBooks = [];
    document.querySelectorAll('.book-checkbox:checked').forEach(checkbox => {
        selectedBooks.push(parseInt(checkbox.value));
    });

    document.getElementById('id_reader_id').value = selectedReader || '';
    document.getElementById('id_book_item_ids').value = JSON.stringify(selectedBooks);

    // Update form panel books display
    const booksDisplay = document.getElementById('selectedBooksDisplay');
    if (booksDisplay) {
        if (selectedBooks.length > 0) {
            const checkedBoxes = document.querySelectorAll('.book-checkbox:checked');
            let booksHtml = '';
            checkedBoxes.forEach(checkbox => {
                const bookItem = checkbox.closest('.book-item');
                const bookTitle = bookItem.querySelector('.font-medium').textContent;
                booksHtml += `<div class="text-xs">• ${bookTitle}</div>`;
            });
            booksDisplay.innerHTML = booksHtml;
        } else {
            booksDisplay.innerHTML = '<em class="text-gray-400">Chưa chọn</em>';
        }
    }

    updateSummary();
    updateSubmitButton();
}

function updateSummary() {
    const config = getConfig();
    const summaryPanel = document.getElementById('summaryPanel');

    if (!summaryPanel) return;

    if (!selectedReader) {
        summaryPanel.innerHTML = '<div class="text-center text-gray-500"><em>Chọn độc giả để xem tóm tắt</em></div>';
        return;
    }

    const reader = readersData.find(r => r.id === selectedReader);
    let html = `<div class="mb-4 pb-4 border-b border-gray-200">
        <strong class="text-gray-700">Độc giả:</strong><br>
        <span class="text-gray-900">${reader.reader_name}</span><br>
        <small class="text-gray-500">${reader.email}</small>
    </div>`;

    if (selectedBooks.length > 0) {
        const checkedBoxes = document.querySelectorAll('.book-checkbox:checked');

        html += `<div class="mb-4 pb-4 border-b border-gray-200">
            <strong class="text-gray-700">Sách trả (${selectedBooks.length} quyển):</strong><br>`;

        checkedBoxes.forEach(checkbox => {
            const bookItem = checkbox.closest('.book-item');
            const bookTitle = bookItem.querySelector('.font-medium').textContent;
            html += `<small class="text-gray-600">• ${bookTitle}</small><br>`;
        });

        html += `</div>`;
    }

    const returnDate = document.getElementById(config.returnDateInputId)?.value;
    if (returnDate) {
        html += `<div class="mb-4">
            <strong class="text-gray-700">Ngày trả:</strong><br>
            <span class="text-gray-900">${new Date(returnDate).toLocaleString('vi-VN')}</span>
        </div>`;
    }

    summaryPanel.innerHTML = html;
}

function updateSubmitButton() {
    const config = getConfig();
    const submitBtn = document.getElementById('submitBtn');
    const hasReader = selectedReader !== null;
    const hasBooks = selectedBooks.length > 0;
    const hasDate = document.getElementById(config.returnDateInputId)?.value;

    submitBtn.disabled = !(hasReader && hasBooks && hasDate);
}

function loadReturnHistory(filter = 'all') {
    const config = getConfig();
    const historyList = document.getElementById('historyList');

    fetch(config.returnBookListUrl + "?filter=" + filter, {
        credentials: 'same-origin'
    })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.text();
        })
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const tableBody = doc.querySelector('tbody');

            if (tableBody && tableBody.innerHTML.trim()) {
                historyList.innerHTML = `
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Phiếu #</th>
                                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Độc giả</th>
                                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Sách</th>
                                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Ngày trả</th>
                                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Tiền phạt</th>
                                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Trạng thái</th>
                            </tr>
                        </thead>
                        <tbody id="historyBody" class="divide-y divide-gray-200"></tbody>
                    </table>
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
            historyList.innerHTML = `<div class="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded">Lỗi tải dữ liệu</div>`;
        });
}
