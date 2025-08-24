import { LitElement, html, css } from '@lit';
import { ContextProvider, ContextConsumer, createContext } from '@lit/context';


export const context = createContext('data');
export const contextOptions = {context, subscribe: true};

// Named panel for content
export class ContentPanel extends LitElement {
    static properties = {
        title: {}
    }

    static styles = css`
        /* A bit of magic to make navigation work properly */
        .offset {
            border-top: 87px solid transparent;
            margin-top: -87px;
        }

        .title-bar {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .title {
            width: fit-content;
            color: var(--text-secondary);
            font-weight: bold;
            white-space: nowrap;
        }

        .line {
            width: 100%;
            height: 1px;
            border-bottom: 2px solid var(--text-secondary);
        }
    `

    constructor() {
        super();
        this.title = "Section";
    }

    render() {
        return html`
            <div class="offset">
                <div class="title-bar">
                    <div class="title">${this.title}</div>
                    <div class="line"></div>
                </div>
                <slot></slot>
            </div>
        `;
    }
}

customElements.define('content-panel', ContentPanel);

// Provides data context for child components
export class DataContext extends LitElement {
    _provider = new ContextProvider(this, {context});

    static properties = {
        dataAttr: { attribute: 'data-attr' }
    }

    set dataAttr(value) {
        this._dataAttr = value;
        this._provider.setValue(document[value]);
    }

    get dataAttr() {
        return this._dataAttr;
    }

    render() {
        return html`<slot></slot>`;
    }
}

customElements.define('data-context', DataContext);


// Displays a table of recipes (filtered)
export class RecipeTable extends LitElement {
    _consumer = new ContextConsumer(this, contextOptions);

    get data() {
        return this._consumer.value;
    }

    static properties = {
        filter: {},
    }

    constructor() {
        super();
        this.filter = {};
    }

    get recipes() {
        // TODO apply filter
        let data = this.data.recipes;

        if (this.filter.station)
            data = data.filter(val => val.station === this.filter.station);

        return data;
    }

    get station() {
        return this.filter.station ?? "All";
    }

    makeIcon(name) {
        let item = this.data.items.find(item => item.name === name);
        let filename = item?.icon ?? "Icon_Warning.png";

        return html`<img src="/images/${filename}" alt=${name} title=${name} width="24" height="24">`;
    }

    makeLine(recipe) {
        let materials = recipe.materials.map(this.makeIcon, this);

        return html`<tr><td>${materials}</td><td>${this.makeIcon(recipe.result)} ${recipe.result}</td></tr>`;
    }

    render() {
        let items = this.recipes.map(this.makeLine, this);

        return html`
            <h3>${this.station} (${this.recipes.length})</h3>
            <table>${items}</table>
        `;
    }
}

customElements.define('recipe-table', RecipeTable);


// Panel with crafting recipes
export class CraftingPanel extends LitElement {
    _consumer = new ContextConsumer(this, contextOptions);

    get data() {
        return this._consumer.value;
    }

    static styles = css`
        :host {
            display: flex;
        }
    `

    render() {
        if (!this.data)
            return html`
                <h1>Loading...</h1>
            `;

        return html`
            <recipe-table .filter=${{station: 'Backpack Printer'}}></recipe-table>
            <recipe-table .filter=${{station: 'Small Printer'}}></recipe-table>
            <recipe-table .filter=${{station: 'Medium Printer'}}></recipe-table>
            <recipe-table .filter=${{station: 'Large Printer'}}></recipe-table>
        `;
    }
}

customElements.define('crafting-panel', CraftingPanel);
