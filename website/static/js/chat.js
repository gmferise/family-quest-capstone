class ChatWidget {
    constructor(element, chatid) {
        this.element = element;
        this.chatid = chatid;

        this.chatsElement = this.element.querySelector(".list-group");
        this.chatElement = this.element.querySelector("#send-chat input");
        this.sendElement = this.element.querySelector("#send-button")

        this.CSRFToken = "";
        this.chats = [];

        this.getChats = this.getChats.bind(this);
        this.sendChat = this.sendChat.bind(this);
        this.resetScroll = this.resetScroll.bind(this);

        this.element.querySelector("#send-chat").addEventListener("submit", (event) => {
            event.preventDefault();
            this.sendChat();
        });

        this.getChats().then(this.resetScroll);
        setInterval(this.getChats, 10000);
    }
    async getChats() {
        this.setLoading(true);
        let res = await fetch(`/api/chat/${this.chatid}/`);
        if (res.ok) {
            this.CSRFToken = res.headers.get("X-CSRFToken");
            this.chats = (await res.json()).messages;
        }
        this.setLoading(false);
    }
    async sendChat() {
        this.setLoading(true);
        let res = await fetch(`/api/chat/${this.chatid}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken":this.CSRFToken
            },
            body: JSON.stringify({
                "content":this.chatElement.value
            })
        });
        if (res.ok) {
            this.CSRFToken = res.headers.get("X-CSRFToken");
            this.chats = (await res.json()).messages;
        }
        this.chatElement.value = "";
        this.setLoading(false);
        this.resetScroll();
    }
    async setLoading(bool) {
        if (bool) {
            this.sendElement.setAttribute("disabled","true");
        } else {
            this.sendElement.removeAttribute("disabled");
            this.chatsElement.innerHTML = "";
            for (let chat of this.chats) {
                let item = document.createElement("div");
                item.classList.add("list-group-item", "list-group-item-action", "py-3");
                item.innerHTML = `
                <div class="d-flex w-100">
                    <a class="portrait me-3" href="/user/${chat.author.account_id}/">
                        <img src="${chat.author.profile || "/static/assets/placeholder.png"}" />
                    </a>
                    <div class="mb-1 flex-grow-1">
                        <div class="d-flex">
                            <a class="text-primary me-auto fs-5 text-ellipsis text-decoration-hover-only"href="/user/${chat.author.account_id}/">${chat.author.name || chat.author.email}</a>
                            <small class="text-muted text-nowrap ms-2">${getDateString(new Date(chat.sent_at))}</small>
                        </div>
                        <div>${chat.content}</div>
                    </div>
                </div>`;
                this.chatsElement.append(item);
            }
        }
    }
    resetScroll() {
        this.chatsElement.scrollBy(0, this.chatsElement.scrollHeight);
    }
}