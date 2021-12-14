import json

correctJson = json.dumps({
    "__class__": "Wrapper",
    "__module__": "knox_source_data_io.models.wrapper",
    "type": "Publication",
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

classifier_gf_json = {
  "__class__": "Wrapper",
  "__module__": "knox_source_data_io.models.wrapper",
  "type": "Publication",
  "schema": "/schema/manuals_v1.3.schema.json",
  "generator": {
    "__class__": "Generator",
    "__module__": "knox_source_data_io.models.wrapper",
    "app": "GrundfosManuals_Handler",
    "version": "1.3.0",
    "generated_at": "2021-11-18 13:28:33.602747"
  },
  "content": {
    "__class__": "Publication",
    "__module__": "knox_source_data_io.models.publication",
    "publisher": "Grundfos A/S",
    "published_at": "",
    "publication": "Grundfosliterature-6253430",
    "pages": 16,
    "articles": [
      {
        "__class__": "Article",
        "__module__": "knox_source_data_io.models.publication",
        "extracted_from": ["/srv/data/grundfosarchive_few_files/Grundfosliterature-6253430.pdf"],
        "confidence": 1.0,
        "page": "1 - 16",
        "headline": "Grundfosliterature-6253430",
        "subhead": "",
        "paragraphs": [
          {
            "__class__": "Paragraph",
            "__module__": "knox_source_data_io.models.publication",
            "kind": "",
            "value": "I am a Grundfos paragraph!",
            "extracted_from": [
              "/srv/data/grundfosarchive_few_files/Grundfosliterature-6253430.pdf"
            ]
          },
          {
            "__class__": "Paragraph",
            "__module__": "knox_source_data_io.models.publication",
            "kind": "",
            "value": "2nd paragraph.",
            "extracted_from": [
              "/srv/data/grundfosarchive_few_files/Grundfosliterature-6253430.pdf"
            ]
          }
        ]
      }
    ]
  }
}

classifier_nj_json = {
    "__class__": "Wrapper",
    "__module__": "knox_source_data_io.models.wrapper",
    "type": "Publication",
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
}