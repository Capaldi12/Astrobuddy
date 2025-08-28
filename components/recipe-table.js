import { LitElement, html, css } from '@lit';
import { ContextConsumer } from '@lit/context';

import { contextOptions } from './data-context.js';

import './item-card.js'


// Displays a table of recipes (filtered)
export default class RecipeTable extends LitElement {
    _consumer = new ContextConsumer(this, contextOptions);

    get data() {
        return this._consumer.value;
    }

    static properties = {

        // TODO split into separate properties?
        filter: {
            converter: {
                fromAttribute: (value, type) => JSON.parse(value),
                toAttribute: (value, type) => JSON.stringify(value)
            },
            reflect: true
        }
    }

    static styles = css`
        td.materials {
            display: flex;
            gap: 0.1em;
        }

        td.result {

        }

        td {
            white-space: nowrap;
        }
    `

    constructor() {
        super();
        this.filter = {};
    }

    get recipes() {
        let data = this.data.recipes;

        if (this.filter.station)
            // TODO check default_station
            data = data.filter(val => val.station === this.filter.station);

        if (this.filter.type)
            // TODO or
            data = data.filter(val => val.type === this.filter.type);

        if (this.filter.result)
            // TODO filter based on resulting item tags
            data = data.filter(val => val.result === this.filter.result);

        if (this.filter.materials)
            this.filter.materials.forEach(material => {
                data = data.filter(val => val.materials.includes(material));
            });

        // TODO other filters

        return data;
    }

    makeLine(recipe) {
        let materials = recipe.materials.map(mat => html`<item-card name=${mat} mode='icon'></item-card>`,);

        return html`
            <tr>
                <td class="materials">
                    ${materials}
                </td>
                <td class="result">
                    <item-card name=${recipe.result} mode='compact'></item-card>
                </td>
            </tr>
        `;
    }

    // This should be somewhere else, but I don't know where to put it yet
    titleCase(str) {
        return str.replace(
            /\w\S*/g,
            text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase()
        );
    }

    // Title to display over the table
    get title() {
        if (this.filter.station)
            return this.filter.station;

        if (this.filter.type)
            return this.titleCase(this.filter.type);

        if (this.filter.result)
            return `For ${this.filter.result}`;

        if (this.filter.materials)
            return `Made from ${this.filter.materials.join(', ')}`

        return "All";
    }

    render() {
        let items = this.recipes.map(this.makeLine, this);

        return html`
            <h3>${this.title} (${this.recipes.length})</h3>
            <table>${items}</table>
        `;
    }
}

customElements.define('recipe-table', RecipeTable);
