const faker = require( 'faker' );
const moment = require('moment');

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