"""
 :mod:`test_frbr_mods` Unit tests for loading MODS xml records into FRBR
                       Redis datastore as native FRBR RDA entities
"""
import unittest,redis,config
from redisco import connection_setup
import lib.frbr_rda as frbr
import lib.mods as mods
from lxml import etree

mods_book_file = open('fixures/modsbook.xml','rb')
mods_book_fixure = mods_book_file.read()
mods_book_file.close()

mods_ejournal_file = open('fixures/modsejournal.xml','rb')
mods_ejournal_fixure = mods_ejournal_file.read()
mods_ejournal_file.close()

mods_motionpicture_file = open('fixures/modsmotionpicture.xml','rb')
mods_motionpicture_fixure = mods_motionpicture_file.read()
mods_motionpicture_file.close()

mods_music_file = open('fixures/modsmusic.xml','rb')
mods_music_fixure = mods_music_file.read()
mods_music_file.close()

redis_server = redis.StrictRedis(host=config.REDIS_HOST,
                                 port=config.REDIS_PORT,
                                 db=config.REDIS_TEST_DB)


connection_setup(host=config.REDIS_HOST,
                 port=config.REDIS_PORT,
                 db=config.REDIS_TEST_DB)


class TestMODSBookToFRBR(unittest.TestCase):

    def setUp(self):
        mods_doc = etree.XML(mods_book_fixure)
        self.mods = mods.mods()
        self.mods.load_xml(mods_doc)
        author_params = {
            'Name': self.mods.names[0]}
        author = frbr.Person(redis_server=redis_server,
                             **author_params)
        work_params = {
            'creators':author,
            'formOfWork':self.mods.typeOfResources[0],
            'subjects':self.mods.subjects,
            'titleOfTheWork':self.mods.titleInfos[0]}
            
            
        self.work = frbr.Work(redis_server=redis_server,
                              **work_params)
        expression_params = {
            'contentTypeExpression':self.mods.genres[0],
            'dateOfExpression':self.mods.originInfos[0].dateIssueds,
            'identifierForTheExpression':self.mods.classifications + self.mods.identifiers,
            'languageOfTheContentExpression':self.mods.languages[0].languageTerms[0]}
        
        self.expression = frbr.Expression(redis_server=redis_server,
                                          **expression_params)

        manifestation_params = {
            'modeOfIssuanceManifestation':self.mods.originInfos[0].issuance,
            'noteOnStatementOfResponsibilityManifestation':self.mods.notes[0],
            'placeOfPublicationManifestation':self.mods.originInfos[0].places,
            'publishersNameManifestation':self.mods.originInfos[0].publishers[0]}
        self.manifestation = frbr.Manifestation(redis_server=redis_server,
                                                **manifestation_params)

    def test_author(self):
        self.assertEquals(self.work.creators.Name.mods_type,
                          'personal')
        self.assertEquals(self.work.creators.Name.authorityURI,
                          "http://id.loc.gov/authorities/names")
        self.assertEquals(self.work.creators.Name.valueURI,
                          "http://id.loc.gov/authorities/names/n92101908")
        self.assertEquals(self.work.creators.Name.nameParts[0].value_of,
                          'Alterman, Eric')
                          
    def test_classifications(self):
         self.assertEquals(self.expression.identifierForTheExpression[0].authority,
                           "lcc")
         self.assertEquals(self.expression.identifierForTheExpression[0].value_of,
                          "PN4888.P6 A48 1999")
         self.assertEquals(self.expression.identifierForTheExpression[1].edition,
                           "21")
         self.assertEquals(self.expression.identifierForTheExpression[1].authority,
                           "ddc")
         self.assertEquals(self.expression.identifierForTheExpression[1].value_of,                  
                           "071/.3")

    def test_content_type(self):
        self.assertEquals(self.expression.contentTypeExpression.value_of,
                          'bibliography')
        self.assertEquals(self.expression.contentTypeExpression.authority,
                          'marcgt')

    def test_date_of_expression(self):
        self.assertEquals(self.expression.dateOfExpression[0].value_of,
                          'c1999')
        self.assertEquals(self.expression.dateOfExpression[1].encoding,
                          "marc")
        self.assertEquals(self.expression.dateOfExpression[1].value_of,
                          "1999")
                          

    def test_form_of_work(self):
        self.assertEquals(self.work.formOfWork.value_of,
                          'text')
                          
    def test_identifiers(self):
        self.assertEquals(self.expression.identifierForTheExpression[2].mods_type,
                          "isbn")
        self.assertEquals(self.expression.identifierForTheExpression[2].value_of,
                          "0801486394 (pbk. : acid-free, recycled paper)")
        self.assertEquals(self.expression.identifierForTheExpression[3].mods_type,
                          "lccn")
        self.assertEquals(self.expression.identifierForTheExpression[3].value_of,
                          "99042030")


    def test_issuance(self):
        self.assertEquals(self.manifestation.modeOfIssuanceManifestation,
                          'monographic')


    def test_language(self):
        self.assertEquals(self.expression.languageOfTheContentExpression.authority,
                          "iso639-2b")
        self.assertEquals(self.expression.languageOfTheContentExpression.mods_type,
                          "code")
        self.assertEquals(self.expression.languageOfTheContentExpression.value_of,
                          "eng")
        self.assertEquals(self.expression.languageOfTheContentExpression.authorityURI,
                          "http://id.loc.gov/vocabulary/iso639-2")
        self.assertEquals(self.expression.languageOfTheContentExpression.valueURI,
                          "http://id.loc.gov/vocabulary/iso639-2/eng")
    

    def test_note_statement_of_responsibility(self):
        self.assertEquals(self.manifestation.noteOnStatementOfResponsibilityManifestation.mods_type,
                          "statement of responsibility")
        self.assertEquals(self.manifestation.noteOnStatementOfResponsibilityManifestation.value_of,
                          "Eric Alterman.")

    def test_place_of_publication(self):
        self.assertEquals(self.manifestation.placeOfPublicationManifestation[0].placeTerms[0].authority,
                          "marccountry")
        self.assertEquals(self.manifestation.placeOfPublicationManifestation[0].placeTerms[0].mods_type,
                          "code")
        self.assertEquals(self.manifestation.placeOfPublicationManifestation[0].placeTerms[0].authorityURI,
                          "http://id.loc.gov/vocabulary/countries")
        self.assertEquals(self.manifestation.placeOfPublicationManifestation[0].placeTerms[0].valueURI,
                          "http://id.loc.gov/vocabulary/countries/nyu")
        self.assertEquals(self.manifestation.placeOfPublicationManifestation[0].placeTerms[0].value_of,
                          "nyu")
        self.assertEquals(self.manifestation.placeOfPublicationManifestation[1].placeTerms[0].mods_type,
                          "text")
        self.assertEquals(self.manifestation.placeOfPublicationManifestation[1].placeTerms[0].value_of,
                          "Ithaca, N.Y")

    def test_publisher(self):
        self.assertEquals(self.manifestation.publishersNameManifestation.value_of,
                          'Cornell University Press')
                          
    

    def test_subject_one(self):
        self.assertEquals(self.work.subjects[0].authority,
                          "lcsh")
        self.assertEquals(self.work.subjects[0].authorityURI,
                          "http://id.loc.gov/authorities/subjects")
    	self.assertEquals(self.work.subjects[0].topics[0].valueURI,
    	                  "http://id.loc.gov/authorities/subjects/sh85070736")
    	self.assertEquals(self.work.subjects[0].topics[0].value_of,
    	                  "Journalism")
    	self.assertEquals(self.work.subjects[0].topics[1].valueURI,
    	                  "http://id.loc.gov/authorities/subjects/sh00005651")
    	self.assertEquals(self.work.subjects[0].topics[1].value_of,
    	                  "Political aspects")
    	self.assertEquals(self.work.subjects[0].geographics[0].valueURI,
    	                  "http://id.loc.gov/authorities/names/n78095330")
    	self.assertEquals(self.work.subjects[0].geographics[0].value_of,
    	                  "United States")
    	                  
    def test_subject_two(self):
        subject = self.work.subjects[1]
        self.assertEquals(subject.authority,"lcsh")
        self.assertEquals(subject.authorityURI,
                          "http://id.loc.gov/authorities/subjects")
        self.assertEquals(subject.geographics[0].valueURI,
                          "http://id.loc.gov/authorities/names/n78095330")
        self.assertEquals(subject.geographics[0].value_of,
                          "United States")
    	self.assertEquals(subject.topics[0].valueURI,
    	                  "http://id.loc.gov/authorities/subjects/sh2002011436")
    	self.assertEquals(subject.topics[0].value_of,
    					  "Politics and government")
    	self.assertEquals(subject.temporals[0].valueURI,
    	                  "http://id.loc.gov/authorities/subjects/sh2002012476")
    	self.assertEquals(subject.temporals[0].value_of,
    	                  "20th century")
    	                  
    def test_subject_three(self):
        subject = self.work.subjects[2]
        self.assertEquals(subject.authority,"lcsh")
        self.assertEquals(subject.authorityURI,
                          "http://id.loc.gov/authorities/subjects")
        self.assertEquals(subject.valueURI,
                          "http://id.loc.gov/authorities/subjects/sh2008107507")
        self.assertEquals(subject.topics[0].valueURI,
                          "http://id.loc.gov/authorities/subjects/sh85081863")
        self.assertEquals(subject.topics[0].value_of,
                          "Mass media")
        self.assertEquals(subject.topics[1].valueURI,
                          "http://id.loc.gov/authorities/subjects/sh00005651")
        self.assertEquals(subject.topics[1].value_of,
                          "Political aspects")
        self.assertEquals(subject.geographics[0].valueURI,
                          "http://id.loc.gov/authorities/names/n78095330")
        self.assertEquals(subject.geographics[0].value_of,
                          "United States")
        
    def test_subject_four(self):
        subject = self.work.subjects[3]
        self.assertEquals(subject.authority,
                          "lcsh")
        self.assertEquals(subject.authorityURI,
                          "http://id.loc.gov/authorities/subjects")
        self.assertEquals(subject.valueURI,
                          "http://id.loc.gov/authorities/subjects/sh2010115992")
        self.assertEquals(subject.topics[0].valueURI,
                          "http://id.loc.gov/authorities/subjects/sh85133490")
        self.assertEquals(subject.topics[0].value_of,
                          "Television and politics")
        self.assertEquals(subject.geographics[0].valueURI,
                         "http://id.loc.gov/authorities/names/n78095330")
        self.assertEquals(subject.geographics[0].value_of,
                          "United States")
                          
    def test_subject_five(self):
        subject = self.work.subjects[4]
        self.assertEquals(subject.authority,
                          "lcsh")
        self.assertEquals(subject.authorityURI,
                          "http://id.loc.gov/authorities/subjects")
        self.assertEquals(subject.valueURI,
                          "http://id.loc.gov/authorities/subjects/sh2008109555")
        self.assertEquals(subject.topics[0].valueURI,
                          "http://id.loc.gov/authorities/subjects/sh85106514")
        self.assertEquals(subject.topics[0].value_of,
                          "Press and politics")
        self.assertEquals(subject.geographics[0].valueURI,
                          "http://id.loc.gov/authorities/names/n78095330")
        self.assertEquals(subject.geographics[0].value_of,
                          "United States")
                          
    def test_subject_six(self):
        subject = self.work.subjects[5]
        self.assertEquals(subject.authority,
                          "lcsh")
        self.assertEquals(subject.authorityURI,
                          "http://id.loc.gov/authorities/subjects")
        self.assertEquals(subject.topics[0].value_of,
                          "Talk shows")
        self.assertEquals(subject.geographics[0].valueURI,
                          "http://id.loc.gov/authorities/names/n78095330")
        self.assertEquals(subject.geographics[0].value_of,
                          "United States")

    def test_title(self):
        self.assertEquals(self.work.titleOfTheWork.title.value_of,
                         'Sound and fury')
        self.assertEquals(self.work.titleOfTheWork.subTitles[0].value_of,
                          'the making of the punditocracy')

    def tearDown(self):
        redis_server.flushdb()

class TestMODSeJournalToFRBR(unittest.TestCase):

    def setUp(self):
        mods_doc = etree.XML(mods_ejournal_fixure)
        self.mods = mods.mods()
        self.mods.load_xml(mods_doc)
        first_author_params = {
            'family':self.mods.names[0].nameParts[0].value_of,
            'given':self.mods.names[0].nameParts[1].value_of}
        first_author = frbr.Person(redis_server=redis_server,
                                   **first_author_params)
        second_author_params = {
            'family':self.mods.names[1].nameParts[0].value_of,
            'given':self.mods.names[1].nameParts[1].value_of}
        second_author = frbr.Person(redis_server=redis_server,
                                    **second_author_params)
        series_work_params = {
            'titleOfTheWork':self.mods.relatedItems[0].titleInfos[0]}
        self.series_work = frbr.Work(redis_server=redis_server,
                                     **series_work_params)
        work_params = {
            'creators':[first_author,second_author],
            'formOfWork':self.mods.typeOfResources[0],
            'titleOfTheWork':self.mods.titleInfos[0],
            'inSeriesWork':self.series_work}
        self.work = frbr.Work(redis_server=redis_server,
                              **work_params)
        expression_params = {
            
            }
        self.expression = frbr.Expression(redis_server=redis_server,
                                          **expression_params)
        manifestation_params = {
            'dateOfPublicationManifestation':self.mods.relatedItems[0].parts[0].dates[0],
            'extentManifestation':self.mods.relatedItems[0].parts[0].extents[0],
            'identifierForTheManifestation':self.mods.identifiers,
            'modeOfIssuanceManifestation':self.mods.relatedItems[0].originInfos[0].issuance,
            'numberingWithinSeriesManifestation':self.mods.relatedItems[0].parts[0].details,
            }
        self.manifestation = frbr.Manifestation(redis_server=redis_server,
                                                **manifestation_params)
        item_params = {
            }
        self.item = frbr.Item(redis_server=redis_server,
                              **item_params)

    def test_authors(self):
        first_author,second_author = self.work.creators[0],self.work.creators[1]
        self.assertEquals(first_author.family,
                          'Testa')
        self.assertEquals(first_author.given,
                          'Bernard')
        self.assertEquals(second_author.family,
                          'Kier')
        self.assertEquals(second_author.given,
                          'Lamont B.')


    def test_extent(self):
        extent = self.manifestation.extentManifestation
        self.assertEquals(extent.unit,
                          "pages")
        self.assertEquals(extent.start,
                          "17")
        self.assertEquals(extent.end,
                          "17")

    def test_form_of_work(self):
        self.assertEquals(self.work.formOfWork.value_of,
                          'text')

    def test_identifiers(self):
        uri_identifier = self.manifestation.identifierForTheManifestation[0]
        self.assertEquals(uri_identifier.mods_type,
                          "uri")
        self.assertEquals(uri_identifier.value_of,
                          'http://www.mdpi.org/entropy/papers/e2010001.pdf')

    def test_issuance(self):
        self.assertEquals(self.manifestation.modeOfIssuanceManifestation,
                          'continuing')

    def test_numbering(self):
        numbering = self.manifestation.numberingWithinSeriesManifestation
        self.assertEquals(numbering[0].mods_type,
                          "volume")
        self.assertEquals(numbering[0].number,
                          "2")
        self.assertEquals(numbering[1].mods_type,
                          "issue")
        self.assertEquals(numbering[1].number,
                          "1")

    def test_publication_date(self):
        publication_date = self.manifestation.dateOfPublicationManifestation
        self.assertEquals(publication_date.value_of,
                          '2000')

    def test_titles(self):
        self.assertEquals(self.work.titleOfTheWork.title.value_of,
                          'Emergence and Dissolvence in the Self-Organization of Complex Systems')
        self.assertEquals(self.work.inSeriesWork.titleOfTheWork.title.value_of,
                          "Entropy")

    

    def tearDown(self):
        redis_server.flushdb()


class TestMODSMotionPictureToFRBR(unittest.TestCase):

    def setUp(self):
        mods_doc = etree.XML(mods_motionpicture_fixure)
        self.mods = mods.mods()
        self.mods.load_xml(mods_doc)
        corporate_body_params = {
            'Name':self.mods.names[0]}
        corporate_body = frbr.CorporateBody(redis_server=redis_server,
                                            **corporate_body_params)
        work_params = {
            'abstract':self.mods.abstracts[0],
            'creators':corporate_body,
            'formOfWork':self.mods.typeOfResources[0],
            'intendedAudienceWork':self.mods.targetAudiences[0],
            'titleOfTheWork':self.mods.titleInfos[0],
            'subjects':self.mods.subjects}
        self.work = frbr.Work(redis_server=redis_server,
                              **work_params)
        expression_params = {
            'contentTypeExpression':self.mods.genres[0],
            'dateOfExpression':self.mods.originInfos[0].dateIssueds[0],
            'languageOfTheContentExpression':self.mods.languages[0].languageTerms[0]}
        self.expression = frbr.Expression(redis_server=redis_server,
                                          **expression_params)

        manifestation_params = {
            'modeOfIssuanceManifestation':self.mods.originInfos[0].issuance,
            'noteManifestation':self.mods.notes[2],
            'noteOnChangesInCarrierCharacteristicsManifestation':self.mods.notes[3],
            'noteOnStatementOfResponsibilityManifestation':self.mods.notes[0],
            'noteOnTitleManifestation':self.mods.notes[1],
            'placeOfProductionManifestation':self.mods.originInfos[0].places,
            'publishersNameManifestation':self.mods.originInfos[0].publishers[0]}
        self.manifestation = frbr.Manifestation(redis_server=redis_server,
                                                **manifestation_params)
        item_params = {
            'extentItem':self.mods.physicalDescriptions[0].extents[0]}
        self.item = frbr.Item(redis_server=redis_server,
                              **item_params)

    def test_abstract(self):
        self.assertEquals(self.work.abstract.value_of,
                          'Shows how cast iron bathtubs are manufactured, illustrating each step from the sculpturing of the wood patterns through the casting and enameling processes.')

    def test_content_type(self):
        self.assertEquals(self.expression.contentTypeExpression.authority,
                          "marcgt")
        self.assertEquals(self.expression.contentTypeExpression.value_of,
                          "motion picture")
            

    def test_corporate_creator(self):
        self.assertEquals(self.work.creators.Name.nameParts[0].value_of,
                          'Walter J. Klein Company')

    def test_date_created(self):
        self.assertEquals(self.expression.dateOfExpression.value_of,
                          '1978')

    def test_extent(self):
        self.assertEquals(self.item.extentItem.value_of,
                          '1 film reel (15 min.) : sd., col. ; 16 mm.')

    def test_form_of_work(self):
        self.assertEquals(self.work.formOfWork.value_of,
                          'moving image')

    def test_intended_audience(self):
        self.assertEquals(self.work.intendedAudienceWork.value_of,
                          'adult')

    def test_issuance(self):
        self.assertEquals(self.manifestation.modeOfIssuanceManifestation,
                          'monographic')

    def test_language(self):
        self.assertEquals(self.expression.languageOfTheContentExpression.authority,
                          "iso639-2b")
        self.assertEquals(self.expression.languageOfTheContentExpression.mods_type,
                          "code")
        self.assertEquals(self.expression.languageOfTheContentExpression.value_of,
                          "eng")


    def test_note_change_carrier_characteristics(self):
        self.assertEquals(self.manifestation.noteOnChangesInCarrierCharacteristicsManifestation.value_of,
                          'Issued also as super 8 mm. and as videorecording.')

    def test_note(self):
        self.assertEquals(self.manifestation.noteManifestation.value_of,
                          'Intended audience: Junior high school students through adults.')
    

    def test_note_statement_of_responsibility(self):
        self.assertEquals(self.manifestation.noteOnStatementOfResponsibilityManifestation.mods_type,
                          "statement of responsibility")
        self.assertEquals(self.manifestation.noteOnStatementOfResponsibilityManifestation.value_of,
                          "Walter J. Klein Company.")

    def test_note_title(self):
        self.assertEquals(self.manifestation.noteOnTitleManifestation.value_of,
                          'Title from data sheet.')

        

    def test_place_of_production(self):
        self.assertEquals(self.manifestation.placeOfProductionManifestation[0].placeTerms[0].authority,
                          'marccountry')
        self.assertEquals(self.manifestation.placeOfProductionManifestation[0].placeTerms[0].mods_type,
                          'code')
        self.assertEquals(self.manifestation.placeOfProductionManifestation[0].placeTerms[0].value_of,
                          'ncu')
        self.assertEquals(self.manifestation.placeOfProductionManifestation[1].placeTerms[0].mods_type,
                          'text')
        self.assertEquals(self.manifestation.placeOfProductionManifestation[1].placeTerms[0].value_of,
                          'Charlotte, N.C')

    def test_publisher(self):
        self.assertEquals(self.manifestation.publishersNameManifestation.value_of,
                          'W.J. Klein Co')
        

    def test_subjects(self):
        self.assertEquals(self.work.subjects[0].authority,
                          'lcsh')
        self.assertEquals(self.work.subjects[0].topics[0].value_of,
                          'Bathtubs')
        self.assertEquals(self.work.subjects[1].authority,
                          'lcsh')
        self.assertEquals(self.work.subjects[1].topics[0].value_of,
                          'Cast-iron')
        self.assertEquals(self.work.subjects[2].authority,
                          'lcsh')
        self.assertEquals(self.work.subjects[2].topics[0].value_of,
                          'Iron-founding')
        self.assertEquals(self.work.subjects[3].authority,
                          'lcshac')
        self.assertEquals(self.work.subjects[3].topics[0].value_of,
                          'Bathtubs')
        self.assertEquals(self.work.subjects[4].authority,
                          'lcshac')
        self.assertEquals(self.work.subjects[4].topics[0].value_of,
                          '<B>Hello World</B>Cast-iron')
        self.assertEquals(self.work.subjects[5].authority,
                          'lcshac')
        self.assertEquals(self.work.subjects[5].topics[0].value_of,
                          'Iron founding')
        
        
        
                          

    def test_title(self):
        self.assertEquals(self.work.titleOfTheWork.title.value_of,
                          'Cast iron story [motion picture] /')
        self.assertEquals(self.work.titleOfTheWork.nonSort,
                          'The ')

    def tearDown(self):
        redis_server.flushdb()
        
class TestMODSMusicPictureToFRBR(unittest.TestCase):

    def setUp(self):
        mods_doc = etree.XML(mods_music_fixure)
        self.mods = mods.mods()
        self.mods.load_xml(mods_doc)
        work_params = {
            'creators':self.mods.names[0],
            'formOfWork':self.mods.typeOfResources[0],
            'titleOfTheWork':self.mods.titleInfos[0]}
        self.work = frbr.Work(redis_server=redis_server,
                              **work_params)
        manifestation_params = {
            'modeOfIssuanceManifestation':self.mods.originInfos[0].issuance}
        self.manifestation = frbr.Manifestation(redis_server=redis_server,
                                                **manifestation_params)
             
    def test_creator(self):
        self.assertEquals(self.work.creators.mods_type,
                          "personal")
        self.assertEquals(self.work.creators.authorityURI,
                          "http://id.loc.gov/authorities/names")
        self.assertEquals(self.work.creators.valueURI,
		          "http://id.loc.gov/authorities/names/n81100426")
	self.assertEquals(self.work.creators.nameParts[0].value_of,
		          "Lawson, Colin (Colin James)")

    def test_form_of_work(self):
        self.assertEquals(self.work.formOfWork.value_of,
                          'notated music')

    def test_issuance(self):
        self.assertEquals(self.manifestation.modeOfIssuanceManifestation,
                          "monographic")
        
    def test_title(self):
        self.assertEquals(self.work.titleOfTheWork.title.value_of,
                          '3 Viennese arias :')
        self.assertEquals(self.work.titleOfTheWork.subTitles[0].value_of,
                          'for soprano, obbligato clarinet in B flat, and piano')
        
    def tearDown(self):
        redis_server.flushdb()
    