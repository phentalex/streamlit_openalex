
def show_result_as_page(articles):
    html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                .keyword-wrapper {
                    background-color: #007bff; /* Синий фон */
                    color: white; /* Белый цвет текста */
                    padding: 5px 10px; /* Отступы внутри обертки */
                    border-radius: 5px; /* Скругление углов */
                    margin-right: 5px; /* Отступ между обертками */
                }
                .MuiListItem-root {
                    padding: 0px;
                    border-bottom: 0px solid #ccc;
                    cursor: pointer;
                }
                .MuiTypography-root {
                    font-family: Roboto, sans-serif;
                }
                .MuiTypography-body1 {
                    font-family: Roboto, sans-serif;
                    font-size: 16px;
                }
                .MuiListItemText-primary {
                    display: block;
                    margin: 8px 0;
                }
                .Muidoc_id-root {
                    color: blue;
                    text-decoration: underline;
                }
                .MuiDivider-root {
                    border: none;
                    border-top: 1px solid #ccc;
                    margin: 2px 0;
                }

                /* Модальное окно */
                .modal {
                    display: none;
                    position: fixed;
                    z-index: 1000; /* Ensure it's above other elements */
                    left: 50%;
                    top: 50%;
                    transform: translate(-50%, -50%);
                    width: 80%;
                    max-height: 60%;
                    overflow-y: auto;
                    background-color: #fff;
                    border: 1px solid #888;
                    border-radius: 15px;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                }
                .modal-content {
                    padding: 20px;
                }
                .close {
                    color: #aaa;
                    float: right;
                    font-size: 28px;
                    font-weight: bold;
                }
                .close:hover,
                .close:focus {
                    color: black;
                    text-decoration: none;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <ul id="articleList"></ul>

            <!-- Модальное окно -->
            <div id="myModal" class="modal">
                <div class="modal-content">
                    <span class="close" onclick="closeModal()">&times;</span>
                    <div id="modalBody" class="modal-body"></div>
                </div>
            </div>

            <script>
    """
    html_code += f"""
                const articles = {articles};
    """
    html_code += """
                const articleList = document.getElementById('articleList');
                const modalBody = document.getElementById('modalBody');

                articles.forEach((article, index) => {
                    const listItem = document.createElement('ul');
                    listItem.className = 'MuiListItem-root';
                    listItem.innerHTML = `
                        <div class="MuiListItemText-root">
                            <span class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary">
                                <b>Название:</b> <span>${article.title || ''}</span>
                            </span>
                        </div>
                        
                        ${article.doi ? `
                        <div class="MuiListItemText-root">
                            <span class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary">
                                <b>Ссылка: </b>
                                <a class="MuiTypography-root MuiTypography-inherit Muidoc_id-root Muidoc_id-underlineAlways" href="${article.doi || ''}" target="_blank">${article.doi}</a>
                            </span>
                        </div>` : ''}

                        ${article.abstract_cut ? `
                        <div class="MuiListItemText-root">
                            <span class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary">
                                <b>Аннотация:</b> <p>${article.abstract_cut}</p>
                            </span>
                        </div>` : ''}
                        
                        ${article.publication_year ? `
                        <div class="MuiListItemText-root">
                            <span class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary">
                                <b>Год публикации:</b> ${article.publication_year}
                            </span>
                        </div>` : ''}

                        <div class="MuiListItemText-root">
                            <span class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary">
                                <b>Число цитирований: </b><span>${article.work_citation}</span>
                            </span>
                        </div>
                        
                        <hr class="MuiDivider-root MuiDivider-fullWidth">
                    `;
                    listItem.addEventListener('click', () => openModal(article));
                    articleList.appendChild(listItem);
                });

                function openModal(article) {
                    modalBody.innerHTML = `
                        <div class="MuiListItemText-root" style="text-align: center; margin-bottom: 25px;">
                            <span class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary" style="font-weight: bold; font-size: 18px;">
                                ${article.title || ''}
                            </span>
                        </div>
                        ${article.keywords ? `
                        <div class="MuiListItemText-root">
                            <span class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary">
                                <b>Тематики (термины):</b> ${article.keywords}
                            </span>
                        </div>` : ''}
                        ${article.doi ? `
                        <div class="MuiListItemText-root">
                            <span class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary">
                                <b>Ссылка: </b>
                                <a class="MuiTypography-root MuiTypography-inherit Muidoc_id-root Muidoc_id-underlineAlways" href="${article.doi || ''}" target="_blank">${article.doi}</a>
                            </span>
                        </div>` : ''}

                        ${article.abstract ? `
                        <div class="MuiListItemText-root">
                            <span class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary">
                                <b>Аннотация:</b> <p>${article.abstract}</p>
                            </span>
                        </div>` : ''}

                        ${article.publication_year ? `
                        <div class="MuiListItemText-root">
                            <span class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary">
                                <b>Год публикации:</b> ${article.publication_year}
                            </span>
                        </div>` : ''}

                        <div class="MuiListItemText-root">
                            <span class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary">
                                <b>Число цитирований: </b><span>${article.work_citation}</span>
                            </span>
                        </div>
                        
                        ${article.type ? `
                        <div class="MuiListItemText-root">
                            <span class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary">
                                <b>Тип публикации:</b> ${article.type}
                            </span>
                        </div>` : ''}
                    `;
                    document.getElementById('myModal').style.display = 'block';
                }

                function closeModal() {
                    document.getElementById('myModal').style.display = 'none';
                }

                window.onclick = function(event) {
                    const modal = document.getElementById('myModal');
                    if (event.target === modal) {
                        modal.style.display = 'none';
                    }
                }
            </script>
        </body>
        </html>
    """
    return html_code

