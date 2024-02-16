export default ({app}, inject) => {
    inject("makeId", (length) => {
        let result = '';
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        const charactersLength = characters.length;
        let counter = 0;
        while (counter < length) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
            counter += 1;
        }
        return result;
    })
}

Array.prototype.extend = function (other_array) {
    other_array.forEach(function (v) {
        this.push(v)
    }, this);
}
