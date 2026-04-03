const API_BASE = "https://api.green-api.com";

const elements = {
  idInstance: document.getElementById("idInstance"),
  apiTokenInstance: document.getElementById("apiTokenInstance"),
  messageChatId: document.getElementById("messageChatId"),
  messageText: document.getElementById("messageText"),
  fileChatId: document.getElementById("fileChatId"),
  fileUrl: document.getElementById("fileUrl"),
  fileName: document.getElementById("fileName"),
  fileCaption: document.getElementById("fileCaption"),
  responseOutput: document.getElementById("responseOutput"),
  statusText: document.getElementById("statusText"),
  clearOutput: document.getElementById("clearOutput"),
  buttons: document.querySelectorAll("[data-action]")
};

const actionConfig = {
  getSettings: {
    method: "GET",
    path: "getSettings"
  },
  getStateInstance: {
    method: "GET",
    path: "getStateInstance"
  },
  sendMessage: {
    method: "POST",
    path: "sendMessage",
    getBody: () => ({
      chatId: requireValue(elements.messageChatId, "Укажите chatId для sendMessage."),
      message: requireValue(elements.messageText, "Введите текст сообщения для sendMessage.")
    })
  },
  sendFileByUrl: {
    method: "POST",
    path: "sendFileByUrl",
    getBody: () => ({
      chatId: requireValue(elements.fileChatId, "Укажите chatId для sendFileByUrl."),
      urlFile: requireValue(elements.fileUrl, "Укажите URL файла для sendFileByUrl."),
      fileName: requireValue(elements.fileName, "Укажите имя файла для sendFileByUrl."),
      caption: elements.fileCaption.value.trim()
    })
  }
};

elements.buttons.forEach((button) => {
  button.addEventListener("click", () => runAction(button.dataset.action));
});

elements.clearOutput.addEventListener("click", () => {
  elements.responseOutput.value = "";
  setStatus("Вывод очищен", "success");
});

async function runAction(actionName) {
  const config = actionConfig[actionName];
  if (!config) {
    return;
  }

  try {
    const credentials = getCredentials();
    const url = `${API_BASE}/waInstance${credentials.idInstance}/${config.path}/${credentials.apiTokenInstance}`;
    const body = config.getBody ? config.getBody() : undefined;

    setBusy(true);
    setStatus(`Выполняется ${actionName}...`);
    writeOutput({
      request: {
        method: config.method,
        url,
        body: body ?? null
      }
    });

    const requestOptions = {
      method: config.method,
      headers: {}
    };

    if (body) {
      requestOptions.headers["Content-Type"] = "application/json";
      requestOptions.body = JSON.stringify(body);
    }

    const response = await fetch(url, requestOptions);
    const rawText = await response.text();
    const parsedBody = tryParseJson(rawText);

    writeOutput({
      request: {
        method: config.method,
        url,
        body: body ?? null
      },
      response: {
        ok: response.ok,
        status: response.status,
        statusText: response.statusText,
        body: parsedBody
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status} ${response.statusText}`);
    }

    setStatus(`${actionName} выполнен успешно`, "success");
  } catch (error) {
    const message = error instanceof Error ? error.message : "Неизвестная ошибка";
    setStatus(message, "error");
  } finally {
    setBusy(false);
  }
}

function getCredentials() {
  const idInstance = requireValue(elements.idInstance, "Укажите idInstance.");
  const apiTokenInstance = requireValue(elements.apiTokenInstance, "Укажите ApiTokenInstance.");

  return { idInstance, apiTokenInstance };
}

function requireValue(element, message) {
  const value = element.value.trim();
  if (!value) {
    element.focus();
    throw new Error(message);
  }

  return value;
}

function tryParseJson(text) {
  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text);
  } catch (_error) {
    return text;
  }
}

function writeOutput(payload) {
  elements.responseOutput.value = JSON.stringify(payload, null, 2);
  elements.responseOutput.scrollTop = 0;
}

function setBusy(isBusy) {
  elements.buttons.forEach((button) => {
    button.disabled = isBusy;
  });
}

function setStatus(text, state = "") {
  elements.statusText.textContent = text;
  const statusBar = elements.statusText.parentElement;
  statusBar.classList.remove("error", "success");

  if (state) {
    statusBar.classList.add(state);
  }
}
