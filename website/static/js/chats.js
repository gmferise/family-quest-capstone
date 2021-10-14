class ChatsWidget {
    constructor(element) {
        this.element = element;

        this.CSRFToken = "";
        this.chats = [];

        this.getChats = this.getChats.bind(this);
        
        this.getChats();
        setInterval(this.getChats, 10000);
    }
    async getChats() {
        this.setLoading(true);
        let count = this.chats.length;
        let res = await fetch("/api/chats/");
        if (res.ok) {
            this.CSRFToken = res.headers.get("X-CSRFToken");
            this.chats = (await res.json()).chats;
        }
        if (this.chats.length > count) {
            this.render();
        }
        this.setLoading(false);
    }
    async createChat() {
        
    }
    async setLoading(bool) {
        if (bool) {
            this.element.classList.add("loading");
        } else {
            this.element.classList.remove("loading");
        }
    }
    render() {
        this.element.innerHTML = "";
        for (let chat of this.chats) {
            let item = document.createElement("a");
            item.classList.add("list-group-item", "list-group-item-action");
            item.href = chat.url;
            let flex = document.createElement("div");
            flex.classList.add("d-flex", "w-100", "justify-content-between");
            let hdr = document.createElement("h5");
            hdr.classList.add("mb-1", "text-ellipsis");
            let label = document.createElement("span");
            label.classList.add("fw-normal");
            label.innerText = chat.members.length === 1 ? "Chat with " : "Group Chat with ";
            let members = document.createElement("span");
            members.classList.add("text-primary");
            members.innerText = chat.members.join(", ");
            hdr.append(label, members);
            let ts = document.createElement("small");
            ts.classList.add("text-muted", "text-nowrap");
            ts.innerText = getDateString(new Date(chat.latestmessage.sent_at));
            flex.append(hdr, ts);
            let msg = document.createElement("p");
            msg.classList.add("mb-1", "text-ellipsis");
            msg.innerText = chat.latestmessage.content;
            let circles = document.createElement("small");
            circles.classList.add("text-muted");
            for (let circle of chat.circles) {
                let badge = document.createElement("span");
                badge.classList.add("badge", "bg-secondary", "me-2");
                badge.innerText = circle;
                circles.append(badge);
            }
            item.append(flex, msg, circles);
            this.element.append(item);
        }
    }
}
class CreateChatForm {
    constructor(formElement) {
        this.element = formElement;
        this.submitButton = formElement.querySelector('button[type="submit"]');
        this.searchElement = formElement.querySelector("#search-users");
        this.suggestionsElement = formElement.querySelector(".suggestions")
        this.listElement = formElement.querySelector("#users-list");
        this.messageElement = formElement.querySelector("#opening-message")
        
        this.suggestions = [];
        this.users = [];

        this.searchUsers = getDebouncer(this.searchUsers.bind(this), 500);
        this.addUser = this.addUser.bind(this);
        this.removeUser = this.removeUser.bind(this);
        this.showSuggestions = this.showSuggestions.bind(this);
        this.submit = this.submit.bind(this);

        this.searchElement.addEventListener("keydown", this.searchUsers);
        this.searchElement.addEventListener("focus", () => this.showSuggestions(true));
        this.searchElement.addEventListener("blur", () => this.showSuggestions(false));
        this.element.addEventListener("submit", this.submit)

        this.showSuggestions(true);
    }

    searchUsers() {
        if (this.searchElement.value === "") {
            this.showSuggestions(false);
            return;
        }
        let res = [];
        for (let i = 0; i < 10; i++) {
            res.push({
                id:Math.floor(Math.random()*4)+1,
                name:['','','','Bill "Billy" Harris Doe','Betsy "Bea" Christine Doe','Timothy "Timmy" Jackson Buck','Albert Jeffery Buck'][Math.floor(Math.random()*7)],
                email:['aaa@gmail.com','bbbbb@gmail.com','bababooey2@gmail.com','dripdrip@drip.net'][Math.floor(Math.random()*4)]
            });
        }
        let ids = this.users.map(user => user.id);
        this.suggestions = res.filter(user => !(ids.includes(user.id)));
        this.renderSuggestions();
    }

    renderSuggestions() {
        this.suggestionsElement.innerHTML = "";
        for (let user of this.suggestions) {
            let item = document.createElement("a");
            item.classList.add("list-group-item", "d-flex", "list-group-item-action");
            let label = document.createElement("div");
            label.classList.add("me-auto", "d-flex", "flex-column");
            if (user.name) {
                label.innerHTML = `
                <div class="text-primary">${user.name}</div>
                <small class="text-muted">${user.email}</div>
                `;
            } else {
                label.innerHTML = `
                <div class="text-primary">${user.email} ${user.id}</div>
                `;
            }
            item.addEventListener("click", () => this.addUser(user));
            item.append(label);
            this.suggestionsElement.append(item);
        }
        this.showSuggestions(true);
    }

    addUser(userobj) {
        this.searchElement.value = "";
        this.users.push(userobj);
        this.searchElement.focus();
        this.suggestions = [];
        this.renderSuggestions();
        this.renderList();
    }

    removeUser(userobj) {
        this.users = this.users.filter(user => user.id !== userobj.id);
        this.renderList();
    }

    showSuggestions(bool) {
        if (bool) {
            //workaround for the fact that height:auto doesn't have transitions
            let preHeight = this.suggestionsElement.clientHeight;
            this.suggestionsElement.style.transitionDuration = "0"; //disable transitions
            this.suggestionsElement.style.height = "auto"; //calc auto height (what it should be)
            let autoHeight = this.suggestionsElement.clientHeight;
            this.suggestionsElement.style.height = preHeight+"px"; //back to what it was
            this.suggestionsElement.style.transitionDuration = ""; //enable transitions
            if (this.suggestionsElement.clientHeight || true) { //forces re-eval of clientHeight for css transition
                this.suggestionsElement.style.height = autoHeight+"px"; //apply auto height and watch the transition fly
            }
        } else {
            this.suggestionsElement.style.height = "0px";
        }
    }

    renderList() {
        this.listElement.innerHTML = `
        <div class="list-group-item d-flex align-items-center text-muted">
            <div class="me-auto">(You)</div>
        </div>`;
        for (let user of this.users) {
            let item = document.createElement("div");
            item.classList.add("list-group-item", "d-flex", "align-items-center");
            let label = document.createElement("div");
            label.classList.add("me-auto");
            label.innerText = (user.name || user.email);
            let closebtn = document.createElement("button");
            closebtn.type = "button";
            closebtn.classList.add("btn-close", "btn-sm");
            closebtn.addEventListener("click", () => this.removeUser(user));
            item.append(label, closebtn);
            this.listElement.append(item);
        }
        if (this.users.length === 0) {
            this.submitButton.setAttribute("disabled", "true");
        } else {
            this.submitButton.removeAttribute("disabled");
        }
    }

    submit() {

    }

}