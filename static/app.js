// static/app.js

let exercisesData = [];
let currentExercise = null;
let currentFilter = 'todos';
let currentUser = null;

function isAuthenticated() {
    return currentUser && currentUser.id && currentUser.id !== "user_default" && currentUser.username;
}

// Monaco Editor Instance & Helper State
let monacoEditor = null;
let pendingCodeToSet = null;

// --- INICIALIZAÇÃO DO MONACO EDITOR (LOCAL) ---
if (window.require) {
    require.config({ paths: { 'vs': '/static/vs' } });
    require(['vs/editor/editor.main'], function () {
        monacoEditor = monaco.editor.create(document.getElementById('monacoEditorContainer'), {
            value: '# Selecione um exercício...',
            language: 'python',
            theme: 'vs-dark',
            automaticLayout: true,
            fontSize: 14,
            lineHeight: 22,
            letterSpacing: 0,
            fontFamily: "Consolas, 'Courier New', monospace",
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            lineNumbers: 'on',
            suggestOnTriggerCharacters: true,
            quickSuggestions: true,
            tabSize: 4,
            cursorBlinking: 'blink',
            cursorStyle: 'line',
            cursorWidth: 2,
            cursorSurroundingLines: 0,
            cursorSmoothCaretAnimation: 'off',
            renderWhitespace: 'none',
            matchBrackets: 'always',
            bracketPairColorization: { enabled: true }
        });

        if (pendingCodeToSet !== null) {
            monacoEditor.setValue(pendingCodeToSet);
            pendingCodeToSet = null;
        }

        // Remedeia a des-sincronização de métricas de fontes web assíncronas
        if (document.fonts && document.fonts.ready) {
            document.fonts.ready.then(function () {
                if (window.monaco && monaco.editor && monaco.editor.remeasureFonts) {
                    monaco.editor.remeasureFonts();
                }
            });
        }
    });
}

// --- INICIALIZAÇÃO DA APLICAÇÃO (MULTI-PAGE APPLICATION) ---
document.addEventListener('DOMContentLoaded', async () => {
    loadSavedUser();

    // Se houver algum Service Worker antigo no navegador, cancela o registro
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.getRegistrations().then(registrations => {
            for (let registration of registrations) {
                registration.unregister();
            }
        });
    }

    const urlParams = new URLSearchParams(window.location.search);
    const exerciseParam = urlParams.get('exercise');

    const exerciseGridElem = document.getElementById('exerciseGrid');
    if (exerciseGridElem) {
        await fetchExercises();
        if (exerciseParam) {
            showEditorView(exerciseParam);
        }
    }
});

// Helpers do Monaco Editor
function getCodeValue() {
    if (monacoEditor) {
        return monacoEditor.getValue();
    }
    return pendingCodeToSet || "";
}

function setCodeValue(code) {
    if (monacoEditor) {
        monacoEditor.setValue(code);
    } else {
        pendingCodeToSet = code;
    }
}

// --- NAVEGAÇÃO ENTRE COMPONENTES DA TELA ---
function showAuthView() {
    const viewAuth = document.getElementById('viewAuth');
    if (!viewAuth) return;

    const viewList = document.getElementById('viewList');
    const viewEditor = document.getElementById('viewEditor');
    const viewHistory = document.getElementById('viewHistory');

    if (viewList) viewList.classList.remove('active');
    if (viewEditor) viewEditor.classList.remove('active');
    if (viewHistory) viewHistory.classList.remove('active');
    if (viewAuth) viewAuth.classList.add('active');

    const btnLogout = document.getElementById('btnLogout');
    if (btnLogout) btnLogout.style.display = 'none';

    switchAuthPageTab('login');
}

function showListView() {
    const viewAuth = document.getElementById('viewAuth');
    const viewList = document.getElementById('viewList');
    const viewEditor = document.getElementById('viewEditor');
    const viewHistory = document.getElementById('viewHistory');

    if (viewAuth) viewAuth.classList.remove('active');
    if (viewEditor) viewEditor.classList.remove('active');
    if (viewHistory) viewHistory.classList.remove('active');
    if (viewList) viewList.classList.add('active');

    const btnLogout = document.getElementById('btnLogout');
    if (btnLogout) btnLogout.style.display = 'inline-flex';

    fetchExercises(); // Atualiza a lista com o progresso atualizado
}

function showHistoryView() {
    if (!isAuthenticated()) {
        showAuthView();
        return;
    }

    const viewAuth = document.getElementById('viewAuth');
    const viewList = document.getElementById('viewList');
    const viewEditor = document.getElementById('viewEditor');
    const viewHistory = document.getElementById('viewHistory');

    if (viewAuth) viewAuth.classList.remove('active');
    if (viewList) viewList.classList.remove('active');
    if (viewEditor) viewEditor.classList.remove('active');
    if (viewHistory) viewHistory.classList.add('active');

    fetchUserHistory();
}

async function showEditorView(exId) {
    if (!isAuthenticated()) {
        showAuthView();
        return;
    }

    currentExercise = exercisesData.find(ex => ex.id === exId);
    if (!currentExercise) return;

    const viewAuth = document.getElementById('viewAuth');
    const viewList = document.getElementById('viewList');
    const viewHistory = document.getElementById('viewHistory');
    const viewEditor = document.getElementById('viewEditor');

    // Se o elemento do editor não existir nesta página (ex: /historico), redireciona com querystring
    if (!viewEditor) {
        window.location.href = `/?exercise=${exId}`;
        return;
    }

    if (viewAuth) viewAuth.classList.remove('active');
    if (viewList) viewList.classList.remove('active');
    if (viewHistory) viewHistory.classList.remove('active');
    if (viewEditor) viewEditor.classList.add('active');

    // Atualiza cabeçalho do editor
    const titleElem = document.getElementById('problemTitle');
    if (titleElem) titleElem.innerText = currentExercise.title;

    const conceptBadge = document.getElementById('problemConceptBadge');
    if (conceptBadge) conceptBadge.innerText = `📌 ${currentExercise.concept || 'Algoritmos & Lógica'}`;

    const badge = document.getElementById('problemLevelBadge');
    if (badge) {
        badge.innerText = currentExercise.level;
        badge.className = `badge badge-${currentExercise.level.toLowerCase()}`;
    }

    // Renderiza a descrição formatada usando Marked.js
    const problemDesc = document.getElementById('problemDescription');
    if (problemDesc) {
        if (window.marked) {
            problemDesc.innerHTML = marked.parse(currentExercise.description);
        } else {
            problemDesc.innerText = currentExercise.description;
        }
    }

    const statusInd = document.getElementById('problemStatusIndicator');
    const statusText = document.getElementById('statusText');
    if (statusInd && statusText) {
        if (currentExercise.passed) {
            statusInd.className = 'status-indicator passed';
            statusText.innerText = 'Resolvido com êxito';
        } else {
            statusInd.className = 'status-indicator';
            statusText.innerText = 'Pendente';
        }
    }

    // Esconde o botão de submissão inicial até os testes passarem
    const btnSubmit = document.getElementById('btnSubmit');
    if (btnSubmit) btnSubmit.classList.add('hidden');

    // Reset console output
    const consoleOut = document.getElementById('consoleOutput');
    if (consoleOut) consoleOut.innerText = '// Clique em "Executar Testes" para avaliar seu código...';

    const banner = document.getElementById('statusBanner');
    if (banner) {
        banner.className = 'console-status-banner';
        banner.innerText = 'Escreva sua solução no centro e clique em "Executar Testes".';
    }

    const execTime = document.getElementById('executionTime');
    if (execTime) execTime.innerText = '-- ms';

    // Carrega o último código salvo do usuário localmente ou no servidor
    try {
        const localSaved = typeof getUserCodeLocal === 'function' ? await getUserCodeLocal(currentUser.id, currentExercise.id) : null;
        if (localSaved && localSaved.code) {
            setCodeValue(localSaved.code);
        } else if (navigator.onLine) {
            const res = await fetch(`/api/user-code/${currentUser.id}/${currentExercise.id}`);
            const data = await res.json();
            setCodeValue(data.code || currentExercise.template);
        } else {
            setCodeValue(currentExercise.template);
        }
    } catch (e) {
        setCodeValue(currentExercise.template);
    }

    setTimeout(() => {
        if (monacoEditor) {
            monacoEditor.layout();
            monacoEditor.focus();
        }
    }, 60);
}

// --- CLIENT APIS LOCAL-FIRST ---
async function fetchExercises() {
    try {
        if (navigator.onLine && currentUser && currentUser.id) {
            const response = await fetch(`/api/exercises?user_id=${currentUser.id}`);
            if (response.ok) {
                exercisesData = await response.json();
            }
        }
    } catch (err) {
        console.warn("Aviso ao buscar exercícios:", err);
    }

    if (!exercisesData || !Array.isArray(exercisesData)) {
        exercisesData = [];
    }

    if (Array.isArray(exercisesData) && currentUser) {
        const passedSet = new Set(exercisesData.filter(ex => ex && ex.passed).map(ex => ex.id));
        currentUser.passed_count = passedSet.size;
        currentUser.total_exercises = exercisesData.length || 30;
        updateUserUI();
    }

    renderExerciseGrid();
}



// --- RENDERIZADOR DO DASHBOARD GRID (TELA 1) ---
function renderExerciseGrid() {
    const gridContainer = document.getElementById('exerciseGrid');
    if (!gridContainer) return;
    gridContainer.innerHTML = '';

    const searchInput = document.getElementById('searchInput');
    const searchTerm = searchInput && searchInput.value ? searchInput.value.toLowerCase().trim() : '';

    if (!exercisesData || !Array.isArray(exercisesData) || exercisesData.length === 0) {
        gridContainer.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">Carregando catálogo de exercícios...</div>';
        return;
    }

    const filtered = exercisesData.filter(ex => {
        if (!ex) return false;
        const title = (ex.title || '').toLowerCase();
        const concept = (ex.concept || '').toLowerCase();
        const level = (ex.level || '').toLowerCase();

        let matchesLevel = false;
        if (currentFilter === 'todos') {
            matchesLevel = true;
        } else if (currentFilter === 'concluidos') {
            matchesLevel = ex.passed === true;
        } else {
            matchesLevel = level === currentFilter.toLowerCase();
        }
        const matchesSearch = title.includes(searchTerm) || concept.includes(searchTerm);
        return matchesLevel && matchesSearch;
    });

    if (filtered.length === 0) {
        gridContainer.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">Nenhum exercício corresponde aos filtros salvos.</div>';
        return;
    }

    filtered.forEach(ex => {
        const card = document.createElement('div');
        card.className = `exercise-card ${ex.passed ? 'passed' : ''}`;
        card.onclick = () => showEditorView(ex.id);

        const badgeClass = `badge-${(ex.level || 'iniciante').toLowerCase()}`;
        const statusIcon = ex.passed
            ? '<span class="status-check">✓ Concluído</span>'
            : '<span style="color: var(--text-muted); font-size: 0.8rem;">Pendente</span>';

        card.innerHTML = `
            <div class="card-top">
                <span class="card-title">${ex.passed ? '✅ ' : ''}${ex.title || ''}</span>
            </div>
            <div class="card-concept">
                📌 ${ex.concept || 'Algoritmos'}
            </div>
            <div class="card-footer">
                <span class="badge ${badgeClass}">${ex.level || 'Iniciante'}</span>
                ${statusIcon}
            </div>
        `;
        gridContainer.appendChild(card);
    });
}

function resetCodeTemplate() {
    if (!currentExercise) return;
    setCodeValue(currentExercise.template);
}

// --- 1. EXECUTAR TESTES (AVALIAÇÃO NO TERMINAL) ---
async function runTests() {
    if (!currentExercise || !currentUser) return;

    const userCode = getCodeValue();
    const btnRun = document.getElementById('btnRunTests');
    const btnSubmit = document.getElementById('btnSubmit');
    const consoleOutput = document.getElementById('consoleOutput');
    const statusBanner = document.getElementById('statusBanner');
    const execTime = document.getElementById('executionTime');

    btnRun.disabled = true;
    btnRun.innerHTML = '⌛ Testando...';
    statusBanner.className = 'console-status-banner';
    statusBanner.innerText = 'Rodando a suíte de testes unitários...';
    consoleOutput.innerText = 'Executando unittest runner em subprocesso...';

    try {
        const response = await fetch('/api/test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                exercise_id: currentExercise.id,
                code: userCode
            })
        });

        const data = await response.json();
        const result = data.result;

        execTime.innerText = `${result.execution_time_ms} ms`;
        consoleOutput.innerText = result.output || result.message;

        if (result.passed) {
            statusBanner.className = 'console-status-banner success';
            statusBanner.innerText = `TODOS OS TESTES PASSARAM! 🎉 - Clique no botão de submissão para salvar sua resposta no banco.`;
            consoleOutput.className = 'console-output success';

            // Exibe e habilita o botão de Submeter Solução
            btnSubmit.classList.remove('hidden');
        } else {
            statusBanner.className = 'console-status-banner failure';
            statusBanner.innerText = `FALHA NOS TESTES ❌ - ${result.message}`;
            consoleOutput.className = 'console-output failure';
            btnSubmit.classList.add('hidden');
        }
    } catch (err) {
        console.error("Erro ao executar testes:", err);
        statusBanner.className = 'console-status-banner failure';
        statusBanner.innerText = 'Erro de Conexão ao executar testes.';
        consoleOutput.className = 'console-output failure';
        consoleOutput.innerText = String(err);
    } finally {
        btnRun.disabled = false;
        btnRun.innerHTML = '<span class="play-icon">▶</span> Executar Testes';
    }
}

// --- 2. SUBMETER SOLUÇÃO (SALVA NO BANCO SQLITE NO SERVIDOR) ---
async function submitSolution() {
    if (!currentExercise || !currentUser) return;

    const userCode = getCodeValue();
    const btnSubmit = document.getElementById('btnSubmit');
    const statusBanner = document.getElementById('statusBanner');

    btnSubmit.disabled = true;
    btnSubmit.innerText = '🚀 Enviando submissão...';

    try {
        const response = await fetch('/api/submissions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                exercise_id: currentExercise.id,
                code: userCode,
                user_id: currentUser ? currentUser.id : undefined
            })
        });

        const data = await response.json();

        if (!response.ok) {
            statusBanner.className = 'console-status-banner error';
            statusBanner.innerText = `ERRO NA SUBMISSÃO: ${data.error || 'Falha ao conectar com o servidor.'}`;
            return;
        }

        const evalResult = data.result;
        if (evalResult && evalResult.passed) {
            currentExercise.passed = true;
            if (currentUser) {
                currentUser.passed_count = (currentUser.passed_count || 0) + 1;
            }
            updateUserUI();

            const statusInd = document.getElementById('problemStatusIndicator');
            if (statusInd) statusInd.className = 'status-indicator passed';
            const statusText = document.getElementById('statusText');
            if (statusText) statusText.innerText = 'Resolvido com êxito';

            statusBanner.className = 'console-status-banner success';
            statusBanner.innerText = `SUBMISSÃO SALVA COM SUCESSO NO SERVIDOR! 🎉 Redirecionando...`;

            setTimeout(() => {
                window.location.href = '/historico';
            }, 800);
        } else {
            statusBanner.className = 'console-status-banner error';
            statusBanner.innerText = `SUBMISSÃO PROCESSADA: ${evalResult ? evalResult.message : 'Falha nos testes'}`;
        }
    } catch (err) {
        console.error("Erro ao submeter solução:", err);
        statusBanner.className = 'console-status-banner error';
        statusBanner.innerText = "Erro ao enviar a submissão para o servidor.";
    } finally {
        btnSubmit.disabled = false;
        btnSubmit.innerText = '🚀 Submeter Solução';
    }
}

// --- FILTROS DE NÍVEL ---
function filterLevel(level) {
    currentFilter = level;
    document.querySelectorAll('.filter-pills .pill').forEach(pill => {
        if (pill.getAttribute('data-filter') === level) {
            pill.classList.add('active');
        } else {
            pill.classList.remove('active');
        }
    });
    renderExerciseGrid();
}

// --- GESTÃO DE USUÁRIOS & NAVBAR UI ---
function loadSavedUser() {
    if (window.SERVER_SESSION_USER) {
        currentUser = window.SERVER_SESSION_USER;
    } else {
        const stored = localStorage.getItem('pycode_user');
        if (stored) {
            try { currentUser = JSON.parse(stored); } catch (e) { currentUser = null; }
        }
    }
    if (!currentUser) {
        currentUser = {
            id: 'user_default',
            username: 'dev_padrao',
            name: 'Desenvolvedor',
            passed_count: 0,
            total_exercises: 30
        };
    }
    updateUserUI();
}

function updateUserUI() {
    if (!currentUser) return;
    const userAvatar = document.getElementById('userAvatar');
    const currentUserName = document.getElementById('currentUserName');
    const userStatsText = document.getElementById('userStatsText');

    const name = currentUser.name || currentUser.username || 'Desenvolvedor';
    if (userAvatar) {
        userAvatar.innerText = name.charAt(0).toUpperCase();
    }
    if (currentUserName) {
        currentUserName.innerText = name;
    }
    if (userStatsText) {
        const passed = currentUser.passed_count !== undefined ? currentUser.passed_count : 0;
        const total = currentUser.total_exercises || 30;
        userStatsText.innerText = `${passed} / ${total} Concluídos 📜`;
    }
}

function saveUserToStorage() {
    if (currentUser) {
        localStorage.setItem('pycode_user', JSON.stringify(currentUser));
    }
}

function openUserModal() {
    const modal = document.getElementById('userModal');
    if (modal) {
        modal.classList.add('active');
        switchAuthTab('login');
        fetchUsers();
    }
}

function closeUserModal() {
    const modal = document.getElementById('userModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// --- GESTÃO DE AUTENTICAÇÃO E TABS ---
function switchAuthPageTab(tabName) {
    const tabLogin = document.getElementById('pageTabLogin') || document.getElementById('tabBtnLogin');
    const tabRegister = document.getElementById('pageTabRegister') || document.getElementById('tabBtnRegister');
    const tabRecover = document.getElementById('pageTabRecover') || document.getElementById('tabBtnRecover');

    const formLogin = document.getElementById('pageLoginForm') || document.getElementById('loginForm');
    const formRegister = document.getElementById('pageRegisterForm') || document.getElementById('registerForm');
    const formRecover = document.getElementById('pageRecoverForm') || document.getElementById('recoverForm');

    hideAuthAlert();

    [tabLogin, tabRegister, tabRecover].forEach(t => t && t.classList.remove('active'));
    [formLogin, formRegister, formRecover].forEach(f => f && f.classList.remove('active'));

    if (tabName === 'login') {
        if (tabLogin) tabLogin.classList.add('active');
        if (formLogin) formLogin.classList.add('active');
    } else if (tabName === 'register') {
        if (tabRegister) tabRegister.classList.add('active');
        if (formRegister) formRegister.classList.add('active');
    } else if (tabName === 'recover') {
        if (tabRecover) tabRecover.classList.add('active');
        if (formRecover) formRecover.classList.add('active');
    }
}

function showAuthAlert(message, type = 'error') {
    const alertBox = document.getElementById('pageAuthAlert') || document.getElementById('authAlert');
    if (alertBox) {
        alertBox.className = `auth-alert ${type}`;
        alertBox.innerText = message;
        alertBox.classList.remove('hidden');
    }
}

function hideAuthAlert() {
    const alertBox = document.getElementById('pageAuthAlert') || document.getElementById('authAlert');
    if (alertBox) {
        alertBox.classList.add('hidden');
        alertBox.innerText = '';
    }
}

async function handleLogout() {
    try {
        if (navigator.onLine) {
            await fetch('/api/auth/logout', { method: 'POST', credentials: 'same-origin' });
        }
    } catch (e) {
        console.warn("Erro ao fazer logout no servidor:", e);
    }
    localStorage.removeItem('pycode_user');
    currentUser = null;
    window.location.href = '/';
}

// --- SUBMISSÃO DE LOGIN ---
async function handleLoginSubmit(e) {
    e.preventDefault();
    hideAuthAlert();

    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;

    if (!username || !password) {
        showAuthAlert('Preencha username e senha.', 'error');
        return;
    }

    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        if (response.ok) {
            currentUser = data.user;
            saveUserToStorage();
            updateUserUI();
            window.location.href = '/dashboard';
            return;
        } else {
            showAuthAlert(data.error || 'Credenciais inválidas.', 'error');
            return;
        }
    } catch (err) {
        console.error("Erro ao conectar com o servidor:", err);
        showAuthAlert('Erro ao conectar ao servidor.', 'error');
    }
}

// --- SUBMISSÃO DE CADASTRO COM USERNAME ÚNICO & E-MAIL CRIPTOGRAFADO ---
async function handleRegisterSubmit(e) {
    e.preventDefault();
    hideAuthAlert();

    const username = document.getElementById('regUsername').value.trim();
    const name = document.getElementById('regName').value.trim() || username;
    const email = document.getElementById('regEmail').value.trim();
    const password = document.getElementById('regPassword').value;

    if (!username || !email || !password) {
        showAuthAlert('Preencha os campos obrigatórios (Username, E-mail e Senha).', 'error');
        return;
    }

    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, name, email, password })
        });

        const data = await response.json();
        if (response.ok) {
            const loginUserElem = document.getElementById('loginUsername');
            if (loginUserElem) loginUserElem.value = username;

            const regUserElem = document.getElementById('regUsername');
            const regNameElem = document.getElementById('regName');
            const regEmailElem = document.getElementById('regEmail');
            const regPassElem = document.getElementById('regPassword');
            if (regUserElem) regUserElem.value = '';
            if (regNameElem) regNameElem.value = '';
            if (regEmailElem) regEmailElem.value = '';
            if (regPassElem) regPassElem.value = '';

            switchAuthPageTab('login');
            showAuthAlert('Conta criada com sucesso! Digite sua senha para acessar.', 'success');
            if (typeof loadExistingUsers === 'function') {
                loadExistingUsers();
            }
            return;
        } else {
            showAuthAlert(data.error || 'Erro ao cadastrar usuário.', 'error');
            return;
        }
    } catch (err) {
        console.error("Erro ao conectar com o servidor:", err);
        showAuthAlert('Erro ao conectar ao servidor.', 'error');
    }
}

// --- SUBMISSÃO DE RECUPERAÇÃO ---
async function handleRecoverSubmit(e) {
    e.preventDefault();
    hideAuthAlert();

    const username = document.getElementById('recoverUsername').value.trim();
    const resultBox = document.getElementById('recoverResult');
    if (resultBox) resultBox.classList.add('hidden');

    if (!username) {
        showAuthAlert('Informe o Username.', 'error');
        return;
    }

    try {
        const response = await fetch('/api/auth/recover', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username })
        });

        const data = await response.json();
        if (response.ok) {
            if (resultBox) {
                resultBox.className = 'recover-result-box';
                resultBox.innerHTML = `
                    <div style="font-weight: 600; color: #10b981; margin-bottom: 0.4rem;">✓ Cadastro Localizado!</div>
                    <div><strong>Nome:</strong> ${data.name} (@${data.username})</div>
                    <div><strong>E-mail de Recuperação:</strong> <code>${data.masked_email}</code></div>
                `;
                resultBox.classList.remove('hidden');
            }
        } else {
            showAuthAlert(data.error || 'Username não encontrado.', 'error');
        }
    } catch (err) {
        showAuthAlert('Erro ao conectar ao servidor para recuperação.', 'error');
    }
}



function updateUserUI() {
    const userNameElem = document.getElementById('currentUserName');
    const userAvatarElem = document.getElementById('userAvatar');
    const userStatsElem = document.getElementById('userStatsText');
    const userBadgeElem = document.getElementById('userBadge');
    const btnHistoryElem = document.getElementById('btnHistory');
    const btnRankingElem = document.getElementById('btnRanking');
    const btnLogoutElem = document.getElementById('btnLogout');
    const btnSwitchUserElem = document.getElementById('btnSwitchUser');

    if (isAuthenticated()) {
        if (userNameElem) userNameElem.innerText = currentUser.name || currentUser.username;
        if (userAvatarElem) userAvatarElem.innerText = (currentUser.name || currentUser.username).charAt(0).toUpperCase();
        if (userStatsElem) userStatsElem.innerText = `${currentUser.passed_count || 0} / 30 Concluídos`;

        if (userBadgeElem) userBadgeElem.style.display = 'flex';
        if (btnHistoryElem) btnHistoryElem.style.display = 'inline-flex';
        if (btnRankingElem) btnRankingElem.style.display = 'inline-flex';
        if (btnLogoutElem) btnLogoutElem.style.display = 'inline-flex';
        if (btnSwitchUserElem) btnSwitchUserElem.style.display = 'none';
    } else {
        if (userBadgeElem) userBadgeElem.style.display = 'none';
        if (btnHistoryElem) btnHistoryElem.style.display = 'none';
        if (btnRankingElem) btnRankingElem.style.display = 'none';
        if (btnLogoutElem) btnLogoutElem.style.display = 'none';
        if (btnSwitchUserElem) btnSwitchUserElem.style.display = 'inline-flex';
    }
}

function saveUserToStorage() {
    if (currentUser) {
        localStorage.setItem('pycode_user', JSON.stringify(currentUser));
    } else {
        localStorage.removeItem('pycode_user');
    }
}

function loadSavedUser() {
    if (window.SERVER_SESSION_USER && window.SERVER_SESSION_USER.id) {
        currentUser = window.SERVER_SESSION_USER;
        saveUserToStorage();
        updateUserUI();
        return true;
    }

    const saved = localStorage.getItem('pycode_user');
    if (saved) {
        try {
            const parsed = JSON.parse(saved);
            if (parsed && parsed.id && parsed.id !== "user_default") {
                currentUser = parsed;
                updateUserUI();
                return true;
            }
        } catch (e) { }
    }
    currentUser = null;
    updateUserUI();
    return false;
}

// --- GESTÃO DE HISTÓRICO DE SUBMISSÕES (FULL PAGE VIEW) ---
let historyData = [];
let currentHistoryFilter = 'todos';

async function fetchUserHistory() {
    const container = document.getElementById('historyListContainer');
    if (container) {
        container.innerHTML = '<div style="text-align: center; padding: 3rem; color: var(--text-muted);">Carregando histórico de submissões...</div>';
    }
    try {
        const userId = (currentUser && currentUser.id) ? currentUser.id : "user_default";
        const response = await fetch(`/api/history/${userId}`);
        historyData = await response.json();
        renderHistoryList();
    } catch (err) {
        console.error("Erro ao carregar histórico:", err);
        if (container) {
            container.innerHTML = '<div style="text-align: center; padding: 3rem; color: var(--accent-red);">Erro de conexão ao carregar histórico.</div>';
        }
    }
}

function filterHistory(filterType) {
    currentHistoryFilter = filterType;
    document.querySelectorAll('[data-history-filter]').forEach(pill => {
        if (pill.getAttribute('data-history-filter') === filterType) {
            pill.classList.add('active');
        } else {
            pill.classList.remove('active');
        }
    });
    renderHistoryList();
}

function renderHistoryList() {
    const container = document.getElementById('historyListContainer');
    const countText = document.getElementById('historyCountText');
    if (!container) return;

    container.innerHTML = '';

    const filtered = historyData.filter(item => {
        if (currentHistoryFilter === 'concluidos') return item.passed === 1;
        return true;
    });

    if (countText) {
        countText.innerText = `${filtered.length} submissão(ões)`;
    }

    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="empty-history" style="text-align: center; padding: 4rem 1rem; color: var(--text-muted); background: var(--bg-card); border-radius: 10px; border: 1px dashed var(--border-color);">
                <h3 style="font-size: 1.1rem; margin-bottom: 0.5rem; color: var(--text-main);">Nenhuma submissão encontrada</h3>
                <p>Nenhuma submissão gravada no histórico para o filtro selecionado.</p>
            </div>
        `;
        return;
    }

    filtered.forEach(item => {
        const historyCard = document.createElement('div');
        historyCard.className = `history-card-item ${item.passed ? 'passed' : 'failed'}`;

        const statusBadge = item.passed
            ? '<span class="history-badge success">✓ Concluído</span>'
            : '<span class="history-badge danger">❌ Falha nos Testes</span>';

        const execTime = item.execution_time_ms ? `${item.execution_time_ms} ms` : '-- ms';
        const rawCode = item.user_code || "# Nenhum código submetido nesta tentativa.";
        const escapedCode = escapeHtml(rawCode);

        historyCard.innerHTML = `
            <div class="history-item-header">
                <div class="history-item-title-group">
                    <span class="history-item-title">${item.exercise_title || item.exercise_id}</span>
                    <span class="badge badge-${(item.exercise_level || 'iniciante').toLowerCase()}">${item.exercise_level || 'Algoritmos'}</span>
                    <span class="concept-badge">📌 ${item.exercise_concept || 'Lógica'}</span>
                    ${statusBadge}
                </div>
                <div class="history-item-meta">
                    <span class="history-time">⏱️ ${execTime}</span>
                    <span class="history-date">🕒 ${item.timestamp}</span>
                </div>
            </div>

            <div class="history-code-panel">
                <div class="code-panel-header">
                    <span class="code-title">🐍 Código Python Submetido</span>
                    <button class="btn btn-sm btn-ghost btn-copy" onclick="copyCodeText(this, \`${escapeJsString(rawCode)}\`)">📋 Copiar Código</button>
                </div>
                <pre class="code-content"><code>${escapedCode}</code></pre>
            </div>

            <div class="history-item-footer">
                <span class="history-status-msg">${escapeHtml(item.message || item.status)}</span>
                <button class="btn btn-secondary btn-sm" onclick="showEditorView('${item.exercise_id}')">
                    📂 Abrir Desafio no Editor →
                </button>
            </div>
        `;
        container.appendChild(historyCard);
    });
}

function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function escapeJsString(str) {
    if (!str) return '';
    return str.replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\$/g, '\\$');
}

function copyCodeText(btn, code) {
    navigator.clipboard.writeText(code).then(() => {
        const origText = btn.innerText;
        btn.innerText = '✓ Copiado!';
        setTimeout(() => { btn.innerText = origText; }, 2000);
    }).catch(err => {
        console.error("Erro ao copiar código:", err);
    });
}

// --- GESTÃO DE RANKING & LEADERBOARD POR NÍVEL ---
async function fetchRanking() {
    const tableBody = document.getElementById('rankingTableBody');
    const countText = document.getElementById('rankingUserCount');

    if (tableBody) {
        tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 2rem; color: var(--text-muted);">Carregando classificação do ranking...</td></tr>';
    }

    try {
        const response = await fetch('/api/ranking');
        const rankingData = await response.json();

        if (countText) {
            countText.innerText = `${rankingData.length} Desenvolvedores Registrados`;
        }

        renderPodium(rankingData.slice(0, 3));
        renderRankingTable(rankingData);
    } catch (err) {
        console.error("Erro ao carregar ranking:", err);
        if (tableBody) {
            tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 2rem; color: var(--accent-red);">Erro de conexão ao carregar ranking.</td></tr>';
        }
    }
}

function renderPodium(top3) {
    const container = document.getElementById('podiumContainer');
    if (!container) return;

    container.innerHTML = '';
    if (!top3 || top3.length === 0) return;

    const podiumOrder = [];
    if (top3[1]) podiumOrder.push({ ...top3[1], pos: 2, medal: '🥈', class: 'podium-silver' });
    if (top3[0]) podiumOrder.push({ ...top3[0], pos: 1, medal: '🥇', class: 'podium-gold' });
    if (top3[2]) podiumOrder.push({ ...top3[2], pos: 3, medal: '🥉', class: 'podium-bronze' });

    podiumOrder.forEach(item => {
        const card = document.createElement('div');
        card.className = `podium-card ${item.class}`;

        const isCurrent = currentUser && currentUser.id === item.id;

        card.innerHTML = `
            <div class="podium-medal">${item.medal}</div>
            <div class="podium-avatar">${item.name.charAt(0).toUpperCase()}</div>
            <h4 class="podium-name">${escapeHtml(item.name)} ${isCurrent ? '<span class="you-tag">(Você)</span>' : ''}</h4>
            <span class="podium-username">@${escapeHtml(item.username)}</span>
            <div class="podium-score">
                <span class="score-number">${item.passed_count}</span>
                <span class="score-total">/ ${item.total_exercises} Concluídos</span>
            </div>
            <div class="podium-breakdown">
                <span class="badge badge-iniciante" title="Iniciante">🌱 ${item.iniciante_count}</span>
                <span class="badge badge-intermediario" title="Intermediário">⚡ ${item.intermediario_count}</span>
                <span class="badge badge-avancado" title="Avançado">🔥 ${item.avancado_count}</span>
            </div>
        `;
        container.appendChild(card);
    });
}

function renderRankingTable(data) {
    const tbody = document.getElementById('rankingTableBody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 2rem;">Nenhum desenvolvedor no ranking ainda.</td></tr>';
        return;
    }

    data.forEach(item => {
        const tr = document.createElement('tr');
        const isCurrent = currentUser && currentUser.id === item.id;

        if (isCurrent) tr.className = 'highlight-current-user';

        let rankBadgeClass = 'rank-num';
        let rankIcon = `#${item.rank}`;
        if (item.rank === 1) { rankIcon = '🥇 #1'; rankBadgeClass = 'rank-num gold'; }
        else if (item.rank === 2) { rankIcon = '🥈 #2'; rankBadgeClass = 'rank-num silver'; }
        else if (item.rank === 3) { rankIcon = '🥉 #3'; rankBadgeClass = 'rank-num bronze'; }

        const percent = Math.round((item.passed_count / item.total_exercises) * 100);

        tr.innerHTML = `
            <td>
                <span class="${rankBadgeClass}">${rankIcon}</span>
            </td>
            <td>
                <div class="ranking-user-info">
                    <span class="ranking-user-name">${escapeHtml(item.name)} ${isCurrent ? '<span class="you-badge">Você</span>' : ''}</span>
                    <span class="ranking-user-sub">@${escapeHtml(item.username)}</span>
                </div>
            </td>
            <td>
                <div class="ranking-progress-group">
                    <span class="progress-text"><strong>${item.passed_count}</strong> / ${item.total_exercises} (${percent}%)</span>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: ${percent}%"></div>
                    </div>
                </div>
            </td>
            <td>
                <div class="level-breakdown-pills">
                    <span class="badge badge-iniciante" title="Iniciante">🌱 ${item.iniciante_count}</span>
                    <span class="badge badge-intermediario" title="Intermediário">⚡ ${item.intermediario_count}</span>
                    <span class="badge badge-avancado" title="Avançado">🔥 ${item.avancado_count}</span>
                </div>
            </td>
            <td>
                ${isCurrent
                ? '<span class="status-indicator passed"><span class="dot"></span> Ativo</span>'
                : '<span style="color: var(--text-muted); font-size: 0.8rem;">Registrado</span>'}
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// --- FEEDBACK VISUAL DE CLIQUE (RIPPLE EFFECT) ---
document.addEventListener('click', function (e) {
    const btn = e.target.closest('.btn, button, .auth-page-tab, .pill');
    if (!btn || btn.closest('#monacoEditorContainer')) return;

    const rect = btn.getBoundingClientRect();
    const circle = document.createElement('span');
    const diameter = Math.max(rect.width, rect.height);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${e.clientX - rect.left - radius}px`;
    circle.style.top = `${e.clientY - rect.top - radius}px`;
    circle.classList.add('click-ripple');

    const existingRipple = btn.getElementsByClassName('click-ripple')[0];
    if (existingRipple) {
        existingRipple.remove();
    }

    btn.appendChild(circle);
    setTimeout(() => circle.remove(), 450);
});
