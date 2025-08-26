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
        filter: {}
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
            data = data.filter(val => val.station === this.filter.station);

        // TODO other filters

        return data;
    }

    get station() {
        return this.filter.station ?? "All";
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

    render() {
        let items = this.recipes.map(this.makeLine, this);

        return html`
            <h3>${this.station} (${this.recipes.length})</h3>
            <table>${items}</table>
        `;
    }
}

customElements.define('recipe-table', RecipeTable);
