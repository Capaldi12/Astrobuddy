import { LitElement, html } from '@lit';
import { ContextProvider, createContext } from '@lit/context';

export const context = createContext('data');
export const contextOptions = {context, subscribe: true};

// Provides data context for child components
export default class DataContext extends LitElement {
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
