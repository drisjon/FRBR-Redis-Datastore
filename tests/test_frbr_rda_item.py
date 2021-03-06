"""
:mod:`test_frbr_rda_item` Tests FRBR RDA Item and supporting
 properties from RDF documents
"""
__author__ = 'Jeremy Nelson'

import logging
import unittest,redis,config
import lib.common as common
import lib.frbr_rda as frbr_rda
import lib.namespaces as ns


redis_server = redis.StrictRedis(host=config.REDIS_HOST,
                                 port=config.REDIS_PORT,
                                 db=config.REDIS_TEST_DB)


class TestItemRDAGroup1Elements(unittest.TestCase):

    def setUp(self):
        self.contact_information_key = "foaf:Person:%s" % redis_server.incr("global:foaf:Person")
        redis_server.set(self.contact_information_key,"Jane Librarian")
        self.custodial_history_of_item_key = "ead:admininfo:custodhist:%s" % redis_server.incr("global:ead:admininfo:custodhist")
        redis_server.set(self.custodial_history_of_item_key,
                         '''The Ocean Falls Corporation records remained in the custody of Pacific Mills Ltd., and its successor companies, until the mill and townsite were taken over by the B.C. provincial government in 1973.''')
        self.dimensions_key = "mods:note:%s" % redis_server.incr("global:mods:note")
        redis_server.hset(self.dimensions_key,
                          "type",
                          "source dimensions")
        redis_server.hset(self.dimensions_key,
                          "value",
                          "Test item dimensions")
        self.dimensions_of_map_key = "mods:note:%s" % redis_server.incr("global:mods:note")
        redis_server.hset(self.dimensions_of_map_key,
                          "type",
                          "source dimensions")
        redis_server.hset(self.dimensions_of_map_key,
                          "value",
                          "Test item dimensions of map")
        self.dimensions_of_still_image_key = None
        redis_server.hset(self.dimensions_of_still_image_key,
                          "type",
                          "source dimensions")
        redis_server.hset(self.dimensions_of_still_image_key,
                          "value",
                          "Test item dimensions of still image")
        self.extent_key = "rdvocab:extent:1093"
        redis_server.set(self.extent_key,
                         "Videodisc")
        self.extent_of_cartographic_resource_key = "rdvocab:extentCarto:1014"
        redis_server.set(self.extent_of_cartographic_resource_key,
                         "Models")
        self.extent_of_notated_music_key = "rdvocab:extenttNoteMus:1018"
        redis_server.set(self.extent_of_notated_music_key,
                         "Vocal scores")
        self.extent_of_still_image_key = "rdvocab:extentImage:1016"
        redis_server.set(self.extent_of_still_image_key,
                         "Wall chart")
        self.extent_of_text_key = "rdvocab:extentText:1002"
        redis_server.set(self.extent_of_text_key,
                         "Leaf")
        self.extent_of_three_dimensional_form_key = "rdvocab:extentThreeDim:1009"
        redis_server.set(self.extent_of_three_dimensional_form_key,
                         "Sculpture")
        self.identifier_for_the_item_key = "mods:identifier:%s" % redis_server.incr("global:mods:identifier")
        redis_server.hset(self.identifier_for_the_item_key,
                          "type",
                          "barcode")
        redis_server.hset(self.identifier_for_the_item_key,
                          "value",
                          "11557800130")
        self.immediate_source_of_acquisition_of_item_key = "frad:CorporateBody:%s" % redis_server.incr("global:frad:CorporateBody")
        redis_server.hset(self.immediate_source_of_acquisition_of_item_key,
                          "name",
                          "Amazon")
        self.item_specific_carrier_characteristic_key = "rdvocab:RDACarrierType:1042"
        redis_server.set(self.item_specific_carrier_characteristic_key,
                         "stereograph card")
        self.item_specific_carrier_characteristic_of_early_printed_resources_key = "rdvocab:RDACarrierType:1048"
        redis_server.set(self.item_specific_carrier_characteristic_of_early_printed_resources_key,
                         "sheet")
        self.note_key = "mods:note:%s" % redis_server.incr("global:mods:note")
        redis_server.set(self.note_key,
                         "Test item note")
        self.note_on_dimensions_of_item_key = "mods:note:%s"  % redis_server.incr("global:mods:note")
        redis_server.hset(self.note_on_dimensions_of_item_key,
                          "type",
                          "source dimensions")
        redis_server.hset(self.note_on_dimensions_of_item_key,
                          "value",
                          "Test note on dimensions of item")
        self.note_on_extent_of_item_key = "mods:note:%s"  % redis_server.incr("global:mods:note")
        redis_server.set(self.note_on_extent_of_item_key,
                         "Test note on extent of item")
        self.preferred_citation_key = "mods:note:%s"  % redis_server.incr("global:mods:note")
        redis_server.hset(self.preferred_citation_key,
                          "type",
                          "preferred citation")
        redis_server.hset(self.preferred_citation_key,
                          "value",
                          "MLA")
        self.restrictions_on_access_key = "mods:accessCondition:%s" % redis_server.incr("global:mods:accessCondition")
        redis_server.hset(self.restrictions_on_access_key,
                          "type",
                          "restriction on access")
        redis_server.hset(self.restrictions_on_access_key,
                          "value",
                          "Test Item restriction on access")
        self.restrictions_on_use_key = "mods:accessCondition:%s" % redis_server.incr("global:mods:accessCondition")
        redis_server.hset(self.restrictions_on_use_key,
                          "type",
                          "use and reproduction")
        redis_server.hset(self.restrictions_on_use_key,
                          "value",
                          "Test Item restriction on use")
        self.uniform_resource_locator_key = "mods:url:%s" % redis_server.incr("global:mods:url")
        redis_server.set(self.uniform_resource_locator_key,
                         "http://example.com/Item")
        params = {'Contact information (Item)':self.contact_information_key, 
                  'Custodial history of item':self.custodial_history_of_item_key, 
                  'Dimensions (Item)':self.dimensions_key,
                  'Dimensions of map, etc. (Item)':self.dimensions_of_map_key, 
                  'Dimensions of still image (Item)':self.dimensions_of_still_image_key, 
                  'Extent (Item)':self.extent_key, 
                  'Extent of cartographic resource (Item)':self.extent_of_cartographic_resource_key, 
                  'Extent of notated music (Item)':self.extent_of_notated_music_key, 
                  'Extent of still image (Item)':self.extent_of_still_image_key, 
                  'Extent of text (Item)':self.extent_of_text_key, 
                  'Extent of three-dimensional form (Item)':self.extent_of_three_dimensional_form_key, 
                  'Identifier for the item':self.identifier_for_the_item_key, 
                  'Immediate source of acquisition of item':self.immediate_source_of_acquisition_of_item_key, 
                  'Item-specific carrier characteristic':self.item_specific_carrier_characteristic_key, 
                  'Item-specific carrier characteristic of early printed resources':self.item_specific_carrier_characteristic_of_early_printed_resources_key, 
                  'Note (Item)':self.note_key,
                  'Note on dimensions of item':self.note_on_dimensions_of_item_key,
                  'Note on extent of item':self.note_on_extent_of_item_key, 
                  'Preferred citation (Item)':self.preferred_citation_key, 
                  'Restrictions on access (Item)':self.restrictions_on_access_key, 
                  'Restrictions on use (Item)':self.restrictions_on_use_key, 
                  'Uniform resource locator (Item)':self.uniform_resource_locator_key}
        self.item = frbr_rda.Item(redis_server=redis_server,
                                  **params)

    def test_init(self):
        self.assert_(self.item.redis_ID)

    def test_contact_information(self):
        contact_information_key = getattr(self.item,
                                          'Contact information (Item)')
        self.assertEquals(self.contact_information_key,
                          contact_information_key)
        self.assertEquals(redis_server.get(contact_information_key),
                          "Jane Librarian")
        
    def test_custodial_history_of_item(self):
        custodial_history_of_item_key = getattr(self.item,
                                                'Custodial history of item')
        self.assertEquals(self.custodial_history_of_item_key,
                          custodial_history_of_item_key)
        self.assertEquals(redis_server.get(custodial_history_of_item_key),
                          '''The Ocean Falls Corporation records remained in the custody of Pacific Mills Ltd., and its successor companies, until the mill and townsite were taken over by the B.C. provincial government in 1973.''')

    def test_dimensions(self):
        dimensions_key = getattr(self.item,
                                 'Dimensions (Item)')
        self.assertEquals(self.dimensions_key,
                          dimensions_key)
        self.assertEquals(redis_server.hget(dimensions_key,
                                            "type"),
                          "source dimensions")
        self.assertEquals(redis_server.hget(dimensions_key,
                                            "value"),
                          "Test item dimensions")

    def dimensions_of_map(self):
        dimensions_of_map_key = getattr(self.item,
                                        'Dimensions of map, etc. (Item)')
        self.assertEquals(dimensions_of_map_key,
                          self.dimensions_of_map_key)
        self.assertEquals(redis_server.hget(dimensions_of_map_key,
                                            "type"),
                          "source dimensions")
        self.assertEquals(redis_server.hget(dimensions_of_map_key,
                                            "value"),
                          "Test item dimensions of map")

    def test_dimensions_of_still_image(self):
        dimensions_of_still_image_key = getattr(self.item,
                                                'Dimensions of still image (Item)')
        self.assertEquals(self.dimensions_of_still_image_key,
                          dimensions_of_still_image_key)
        self.assertEquals(redis_server.hget(dimensions_of_still_image_key,
                                            "type"),
                          "source dimensions")
        self.assertEquals(redis_server.hget(dimensions_of_still_image_key,
                                            "value"),
                          "Test item dimensions of still image")
        
    def test_extent(self):
        extent_key = getattr(self.item,
                             'Extent (Item)')
        self.assertEquals(self.extent_key,
                          extent_key)
        self.assertEquals(redis_server.get(extent_key),
                          "Videodisc")

    def test_extent_of_cartographic_resource(self):
        extent_of_cartographic_resource_key = getattr(self.item,
                                                      'Extent of cartographic resource (Item)')
        self.assertEquals(self.extent_of_cartographic_resource_key,
                          extent_of_cartographic_resource_key)
        self.assertEquals(redis_server.get(extent_of_cartographic_resource_key),
                          "Models")

    def test_extent_of_notated_music(self):
        extent_of_notated_music_key = getattr(self.item,
                                              'Extent of notated music (Item)')
        self.assertEquals(self.extent_of_notated_music_key,
                          extent_of_notated_music_key)
        self.assertEquals(redis_server.get(extent_of_notated_music_key),
                          "Vocal scores")

    def test_extent_of_still_image(self):
        extent_of_still_image_key = getattr(self.item,
                                            'Extent of still image (Item)')
        self.assertEquals(self.extent_of_still_image_key,
                          extent_of_still_image_key)
        self.assertEquals(redis_server.get(extent_of_still_image_key),
                          "Wall chart")

    def test_extent_of_text(self):
        extent_of_text_key = getattr(self.item,
                                     'Extent of text (Item)')
        self.assertEquals(self.extent_of_text_key,
                          extent_of_text_key)

        self.assertEquals(redis_server.get(extent_of_text_key),
                          "Leaf")

    def test_extent_of_three_dimensional_form(self):
        extent_of_three_dimensional_form_key = getattr(self.item,
                                                       'Extent of three-dimensional form (Item)')
        self.assertEquals(self.extent_of_three_dimensional_form_key,
                          extent_of_three_dimensional_form_key)
        self.assertEquals(redis_server.get(extent_of_three_dimensional_form_key),
                          "Sculpture")

    def test_identifier_for_the_item(self):
        identifier_for_the_item_key = getattr(self.item,
                                              'Identifier for the item')
        self.assertEquals(self.identifier_for_the_item_key,
                          identifier_for_the_item_key)
        self.assertEquals(redis_server.hget(identifier_for_the_item_key,
                                            "type"),
                          "barcode")
        self.assertEquals(redis_server.hget(identifier_for_the_item_key,
                                            "value"),
                          "11557800130")

    def test_immediate_source_of_acquisition_of_item(self):
        immediate_source_of_acquisition_of_item_key = getattr(self.item,
                                                              'Immediate source of acquisition of item')
        self.assertEquals(self.immediate_source_of_acquisition_of_item_key,
                          immediate_source_of_acquisition_of_item_key)
        self.assertEquals(redis_server.hget(immediate_source_of_acquisition_of_item_key,
                                            "name"),
                          "Amazon")
    def test_item_specific_carrier_characteristic(self):
        item_specific_carrier_characteristic_key = getattr(self.item,
                                                           'Item-specific carrier characteristic')
        self.assertEquals(self.item_specific_carrier_characteristic_key,
                          item_specific_carrier_characteristic_key)
        self.assertEquals(redis_server.get(item_specific_carrier_characteristic_key),
                          "stereograph card")

    def test_item_specific_carrier_characteristic_of_early_printed_resources(self):
        item_specific_carrier_characteristic_of_early_printed_resources_key = getattr(self.item,
                                                                                      'Item-specific carrier characteristic of early printed resources')
        self.assertEquals(self.item_specific_carrier_characteristic_of_early_printed_resources_key,
                          item_specific_carrier_characteristic_of_early_printed_resources_key)
        self.assertEquals(redis_server.get(item_specific_carrier_characteristic_of_early_printed_resources_key),
                          "sheet")

    def test_note(self):
        note_key = getattr(self.item,
                           'Note (Item)')
        self.assertEquals(self.note_key,
                          note_key)
        self.assertEquals(redis_server.get(self.note_key),
                          "Test item note")

    def test_note_on_dimensions_of_item(self):
        note_on_dimensions_of_item_key = getattr(self.item,
                                                 'Note on dimensions of item')
        self.assertEquals(self.note_on_dimensions_of_item_key,
                          note_on_dimensions_of_item_key)
        self.assertEquals(redis_server.hget(note_on_dimensions_of_item_key,
                                            "type"),
                          "source dimensions")
        self.assertEquals(redis_server.hget(note_on_dimensions_of_item_key,
                                            "value"),
                          "Test note on dimensions of item")
        
    def test_note_on_extent_of_item(self):
        note_on_extent_of_item_key = getattr(self.item,
                                             'Note on extent of item')
        self.assertEquals(self.note_on_extent_of_item_key,
                          note_on_extent_of_item_key)
        
        self.assertEquals(redis_server.get(note_on_extent_of_item_key),
                          "Test note on extent of item")

    def test_preferred_citation(self):
        preferred_citation_key = getattr(self.item,
                                         'Preferred citation (Item)')
        self.assertEquals(self.preferred_citation_key,
                          preferred_citation_key)
        self.assertEquals(redis_server.hget(preferred_citation_key,
                                            "type"),
                          "preferred citation")
        self.assertEquals(redis_server.hget(preferred_citation_key,
                                            "value"),
                          "MLA")

    def test_restrictions_on_access(self):
        restrictions_on_access_key = getattr(self.item,
                                             'Restrictions on access (Item)')
        self.assertEquals(self.restrictions_on_access_key,
                          restrictions_on_access_key)
        self.assertEquals(redis_server.hget(restrictions_on_access_key,
                                            "type"),
                          "restriction on access")
        self.assertEquals(redis_server.hget(restrictions_on_access_key,
                                            "value"),
                          "Test Item restriction on access")

    def test_restrictions_on_use(self):
        restrictions_on_use_key =  getattr(self.item,
                                           'Restrictions on use (Item)')
        self.assertEquals(self.restrictions_on_use_key,
                          restrictions_on_use_key)
        self.assertEquals(redis_server.hget(restrictions_on_use_key,
                                            "type"),
                          "use and reproduction")
        self.assertEquals(redis_server.hget(self.restrictions_on_use_key,
                                            "value"),
                          "Test Item restriction on use")

    def test_uniform_resource_locator(self):
        uniform_resource_locator_key = getattr(self.item,
                                               'Uniform resource locator (Item)')
        self.assertEquals(self.uniform_resource_locator_key,
                          uniform_resource_locator_key)
        self.assertEquals(redis_server.get(uniform_resource_locator_key),
                          "http://example.com/Item")

    def tearDown(self):
        redis_server.flushdb()

class TestItemWEMIRelationships(unittest.TestCase):
 
    def setUp(self):
        self.accompanied_by_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.analysis_of_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.bound_with_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.commentary_on_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.contained_in_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.contains_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.critique_of_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.description_of_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.descriptive_relationships_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.digital_transfer_of_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.electronic_reproduction_of_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.equivalence_relationships_key = "frbr:Item:%s" % redis_server.incr("global:frbr:Item")
        self.evaluation_of_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.facsimile_of_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.filmed_with_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.manifestation_exemplified_key = "frbr_rda:Manifestation:%s" % redis_server.incr("global:frbr_rda:Manifestation")
        self.on_disc_with_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.preservation_facsimile_of_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.reprint_of_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.reproduction_of_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.review_of_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.sequential_relationship_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        self.whole_part_relationship_key = "frbr_rda:Item:%s" % redis_server.incr("global:frbr_rda:Item")
        params = {'Accompanied by (Item)':self.accompanied_by_key,
                  'Analysis of (Item)':self.analysis_of_key,
                  'Bound with (Item)':self.bound_with_key,
                  'Commentary on (Item)':self.commentary_on_key,
                  'Contained in (item)':self.contained_in_key,
                  'Contains (Item)':self.contains_key,
                  'Critique of (Item)':self.critique_of_key,
                  'Description of (Item)':self.description_of_key,
                  'Descriptive relationships (Item)':self.descriptive_relationships_key,
                  'Digital transfer of (Item)':self.digital_transfer_of_key,
                  'Electronic reproduction of (Item)':self.electronic_reproduction_of_key,
                  'Equivalence relationships (Item)':self.equivalence_relationships_key,
                  'Evaluation of (Item)':self.evaluation_of_key,
                  'Facsimile of (Item)':self.facsimile_of_key,
                  'Filmed with (Item)':self.filmed_with_key,
                  'Manifestation exemplified':self.manifestation_exemplified_key,
                  'On disc with (Item)':self.on_disc_with_key,
                  'Preservation facsimile of (Item)':self.preservation_facsimile_of_key,
                  'Reprint of (Item)':self.reprint_of_key,
                  'Reproduction of (Item)':self.reproduction_of_key,
                  'Review of (Item)':self.review_of_key,
                  'Sequential relationship (Item)':self.sequential_relationship_key,
                  'Whole-part relationship (Item)':self.whole_part_relationship_key}
        self.item = frbr_rda.Item(redis_server=redis_server,
                                  **params)


    def test_init(self):
        self.assert_(self.item.redis_ID)

    def test_accompanied_by(self):
        self.assertEquals(getattr(self.item,'Accompanied by (Item)'),
                          self.accompanied_by_key)

    def test_analysis_of(self):
        self.assertEquals(getattr(self.item,'Analysis of (Item)'),
                          self.analysis_of_key)

    def test_bound_with(self):
        self.assertEquals(getattr(self.item,'Bound with (Item)'),
                          self.bound_with_key)

    def test_commentary_on(self):
        self.assertEquals(getattr(self.item,'Commentary on (Item)'),
                          self.commentary_on_key)

    def test_contained_in(self):
        self.assertEquals(getattr(self.item,'Contained in (item)'),
                          self.contained_in_key)

    def test_contains(self):
        self.assertEquals(getattr(self.item,'Contains (Item)'),
                          self.contains_key)

    def test_critique_of(self):
        self.assertEquals(getattr(self.item,'Critique of (Item)'),
                          self.critique_of_key)

    def test_description_of(self):
        self.assertEquals(getattr(self.item,'Description of (Item)'),
                          self.description_of_key)

    def test_descriptive_relationships(self):
        self.assertEquals(getattr(self.item,'Descriptive relationships (Item)'),
                          self.descriptive_relationships_key)

    def test_digital_transfer_of(self):
        self.assertEquals(getattr(self.item,'Digital transfer of (Item)'),
                          self.digital_transfer_of_key)

    def test_electronic_reproduction_of(self):
        self.assertEquals(getattr(self.item,'Electronic reproduction of (Item)'),
                          self.electronic_reproduction_of_key)

    def test_equivalence_relationships(self):
        self.assertEquals(getattr(self.item,'Equivalence relationships (Item)'),
                          self.equivalence_relationships_key)

    def test_evaluation_of(self):
        self.assertEquals(getattr(self.item,'Evaluation of (Item)'),
                          self.evaluation_of_key)
        

    def test_facsimile_of(self):
        self.assertEquals(getattr(self.item,'Facsimile of (Item)'),
                          self.facsimile_of_key)

    def test_filmed_with(self):
        self.assertEquals(getattr(self.item,'Filmed with (Item)'),
                          self.filmed_with_key)

    def test_manifestation_exemplified(self):
        self.assertEquals(getattr(self.item,'Manifestation exemplified'),
                          self.manifestation_exemplified_key)

    def test_on_disc_with(self):
        self.assertEquals(getattr(self.item,'On disc with (Item)'),
                          self.on_disc_with_key)

    def test_preservation_facsimile_of(self):
        self.assertEquals(getattr(self.item,'Preservation facsimile of (Item)'),
                          self.preservation_facsimile_of_key)

    def test_reprint_of(self):
        self.assertEquals(getattr(self.item,'Reprint of (Item)'),
                          self.reprint_of_key)

    def test_reproduction_of(self):
        self.assertEquals(getattr(self.item,'Reproduction of (Item)'),
                          self.reproduction_of_key)

    def test_review_of(self):
        self.assertEquals(getattr(self.item,'Review of (Item)'),
                          self.review_of_key)

    def test_sequential_relationship(self):
        self.assertEquals(getattr(self.item,'Sequential relationship (Item)'),
                          self.sequential_relationship_key)

    def test_whole_part_relationship(self):
        self.assertEquals(getattr(self.item,'Whole-part relationship (Item)'),
                          self.whole_part_relationship_key)

    def tearDown(self):
        redis_server.flushdb()
