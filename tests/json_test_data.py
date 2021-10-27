import json

correctJson = json.dumps({
    "__class__": "Wrapper",
    "__module__": "knox_source_data_io.models.wrapper",
    "type": "Schema_Article",
    "schema": "TestSchema",
    "generator": {
        "app": "This App",
        "version": "0.0.0.1",
        "generated_at": "Some time ago"
    },
    "content": {
        "__class__": "Publication",
        "__module__": "knox_source_data_io.models.publication",
        "publication": "Publication1",
        "published_at": "2018-03-27T00:00:00+02:00",
        "publisher": "NordJyskePublisher",
        "pages": 3,
        "articles": [
            {
                "__class__": "Article",
                "__module__": "knox_source_data_io.models.publication",
                "headline": "This is head line",
                "id": 0,
                "extracted_from": [
                    "This if file 1",
                    "This is file 2"
                ],
                "paragraphs": [
                    {
                        "__class__": "Paragraph",
                        "__module__": "knox_source_data_io.models.publication",
                        "kind": "What kind?",
                        "value": "Jens Hansen havde en bondegård."
                    },
                    {
                        "__class__": "Paragraph",
                        "__module__": "knox_source_data_io.models.publication",
                        "kind": "This Kind!",
                        "value": "E I E I O!"
                    }
                ],
                "byline": {
                    "__class__": "Byline",
                    "__module__": "knox_source_data_io.models.publication",
                    "name": "Michael Jackson",
                    "email": "MJ@king_of_pop.org"
                }
            },{
                "__class__": "Article",
                "__module__": "knox_source_data_io.models.publication",
                "headline": "This is different headline",
                "id": 1,
                "paragraphs": [
                    {
                        "__class__": "Paragraph",
                        "__module__": "knox_source_data_io.models.publication",
                        "kind": "No",
                        "value": "Aalborg er en dansk by i Nordjylland."
                    },
                    {
                        "__class__": "Paragraph",
                        "__module__": "knox_source_data_io.models.publication",
                        "kind": "Yes",
                        "value": "Lego er ikke lokaliseret i Aalborg."
                    }
                ]
            }
        ]
    }
})

incorrectJson = json.dumps({
    "type": "Schema_Article",
    "schema": "TestSchema",
    "generator": {
        "app": "This App",
        "version": "0.0.0.1",
        "generated_at": "Some time ago"
    },
    "content": {
        "__class__": "Publication",
        "__module__": "knox_source_data_io.models.publication",
        "publication": "Publication1",
        "published_at": "2018-03-27T00:00:00+02:00",
        "publisher": "NordJyskePublisher",
        "pages": 3,
        "articles": [
            {
                "__class__": "Article",
                "__module__": "knox_source_data_io.models.publication",
                "headline": "This is head line",
                "id": 0,
                "extracted_from": [
                    "This if file 1",
                    "This is file 2"
                ],
                "paragraphs": [
                    {
                        "__class__": "Paragraph",
                        "__module__": "knox_source_data_io.models.publication",
                        "kind": "What kind?",
                        "value": "Jens Hansen havde en bondegård."
                    },
                    {
                        "__class__": "Paragraph",
                        "__module__": "knox_source_data_io.models.publication",
                        "kind": "This Kind!",
                        "value": "E I E I O!"
                    }
                ],
                "byline": {
                    "__class__": "Byline",
                    "__module__": "knox_source_data_io.models.publication",
                    "name": "Michael Jackson",
                    "email": "MJ@king_of_pop.org"
                }
            },{
                "__class__": "Article",
                "__module__": "knox_source_data_io.models.publication",
                "headline": "This is different headline",
                "id": 1,
                "paragraphs": [
                    {
                        "__class__": "Paragraph",
                        "__module__": "knox_source_data_io.models.publication",
                        "kind": "No",
                        "value": "Aalborg er en dansk by i Nordjylland."
                    },
                    {
                        "__class__": "Paragraph",
                        "__module__": "knox_source_data_io.models.publication",
                        "kind": "Yes",
                        "value": "Lego er ikke lokaliseret i Aalborg."
                    }
                ]
            }
        ]
    }
})