from flask_restful import fields


section = {
    "id" :fields.Integer,
    "section_name":fields.String,
    "description":fields.String,
    "date_created":fields.DateTime
}

sections = {
    "sections":fields.List(fields.Nested(section))
}