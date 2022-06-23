const faker = require( 'faker' );
const moment = require('moment');
let levelzerointerests = require('./interests.json');

let unlockedInterests = [];
for(let i=0 ; i < 6 ; i++){
    var r = Math.floor(Math.random() * levelzerointerests.length);
    unlockedInterests.push(levelzerointerests[r]);
    levelzerointerests.splice(r, 1);
}

exports.createRandomUser = (req, context, events, next) => {
    var levelpercentage = (Math.floor(Math.random() * ( 9 - 1 + 1)) + 1)*10
    var currentdate = moment().format("DD/MM/YYYY")
    var userpayload = {
        "id":"",
        "name":"",
        "email":"",
        "urlphoto":"",
        "registrationdate":currentdate,
        "levelpercentage": levelpercentage
    };
    userpayload.id = "performancetestuser"+faker.datatype.uuid();
    userpayload.name = faker.name.findName();
    userpayload.email = faker.internet.email();
    userpayload.urlphoto = faker.image.avatar();
    context.vars.userpayload = userpayload;
    return next();
}

exports.getCurrentDate = (req, context, events, next) => {
    const currentdate = moment().format("DD/MM/YYYY");
    context.vars.currentdate = currentdate;
    return next();
}

exports.selectRandomInterests = (req, context, events, next) => {
    context.vars.unlockedInterests = unlockedInterests;
    context.vars.boxesInterests = levelzerointerests;
    return next()
}
