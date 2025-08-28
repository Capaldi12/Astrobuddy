import { LitElement, html, css } from '@lit';
import { ContextConsumer } from '@lit/context';

import { contextOptions } from './data-context.js';

import './recipe-table.js';


// Panel with crafting recipes
export default class CraftingPanel extends LitElement {
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
            <div>
                <recipe-table .filter=${{type: 'refining'}}></recipe-table>
                <recipe-table .filter=${{type: 'chemistry'}}></recipe-table>
            </div>

        `;
    }
}

customElements.define('crafting-panel', CraftingPanel);
