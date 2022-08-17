from ecgai_drawing.enums.color_style import ColorStyle
from ecgai_drawing.enums.ecg_lead_name import LeadName


class OrderedEnumTestObject(object):
    def __init__(self, lead: LeadName):
        self.lead = lead

    def __lt__(self, other):
        return self.lead < other.lead


# noinspection DuplicatedCode
def get_ecg_leads_list() -> list[OrderedEnumTestObject]:
    enum_list = list[OrderedEnumTestObject]()

    lead1 = OrderedEnumTestObject(lead=LeadName.V1)
    enum_list.append(lead1)

    lead2 = OrderedEnumTestObject(lead=LeadName.II)
    enum_list.append(lead2)

    lead3 = OrderedEnumTestObject(lead=LeadName.I)
    enum_list.append(lead3)

    lead4 = OrderedEnumTestObject(lead=LeadName.V3)
    enum_list.append(lead4)

    lead5 = OrderedEnumTestObject(lead=LeadName.V2)
    enum_list.append(lead5)

    lead6 = OrderedEnumTestObject(lead=LeadName.III)
    enum_list.append(lead6)

    lead7 = OrderedEnumTestObject(lead=LeadName.V6)
    enum_list.append(lead7)

    lead8 = OrderedEnumTestObject(lead=LeadName.V5)
    enum_list.append(lead8)

    lead9 = OrderedEnumTestObject(lead=LeadName.V4)
    enum_list.append(lead9)

    lead10 = OrderedEnumTestObject(lead=LeadName.aVF)
    enum_list.append(lead10)

    lead11 = OrderedEnumTestObject(lead=LeadName.aVL)
    enum_list.append(lead11)

    lead12 = OrderedEnumTestObject(lead=LeadName.aVR)
    enum_list.append(lead12)
    return enum_list


# noinspection DuplicatedCode
def test_unsorted_ecg_lead_enum():
    sut = get_ecg_leads_list()
    lead1 = sut[0].lead
    lead2 = sut[1].lead
    lead3 = sut[2].lead
    lead4 = sut[3].lead
    lead5 = sut[4].lead
    lead6 = sut[5].lead
    lead7 = sut[6].lead
    lead8 = sut[7].lead
    lead9 = sut[8].lead
    lead10 = sut[9].lead
    lead11 = sut[10].lead
    lead12 = sut[11].lead
    assert lead1 == LeadName.V1
    assert lead2 == LeadName.II
    assert lead3 == LeadName.I
    assert lead4 == LeadName.V3
    assert lead5 == LeadName.V2
    assert lead6 == LeadName.III
    assert lead7 == LeadName.V6
    assert lead8 == LeadName.V5
    assert lead9 == LeadName.V4
    assert lead10 == LeadName.aVF
    assert lead11 == LeadName.aVL
    assert lead12 == LeadName.aVR
    assert len(sut) == 12


# noinspection DuplicatedCode
def test_sorted_ecg_lead_enum():
    sut = get_ecg_leads_list()
    sut.sort()
    lead1 = sut[0].lead
    lead2 = sut[1].lead
    lead3 = sut[2].lead
    lead4 = sut[3].lead
    lead5 = sut[4].lead
    lead6 = sut[5].lead
    lead7 = sut[6].lead
    lead8 = sut[7].lead
    lead9 = sut[8].lead
    lead10 = sut[9].lead
    lead11 = sut[10].lead
    lead12 = sut[11].lead
    assert lead1 == LeadName.I
    assert lead2 == LeadName.II
    assert lead3 == LeadName.III
    assert lead4 == LeadName.aVR
    assert lead5 == LeadName.aVL
    assert lead6 == LeadName.aVF
    assert lead7 == LeadName.V1
    assert lead8 == LeadName.V2
    assert lead9 == LeadName.V3
    assert lead10 == LeadName.V4
    assert lead11 == LeadName.V5
    assert lead12 == LeadName.V6
    assert len(sut) == 12


def test_convert_from_string_to_ecg_lead_enum():
    lead1 = LeadName["V6"]
    assert lead1 == LeadName.V6


def test_convert_from_string_lower_case_to_ecg_lead_enum():
    lead1 = LeadName["avl"]
    assert lead1 == LeadName.aVL


def test_convert_from_string_to_ecg_lead_enum_unknown_lead_name():
    lead1 = LeadName["testing"]
    assert lead1 == LeadName.Unknown


def test_ecg_lead_enum_to_string_from_lower_case():
    lead1 = LeadName["avl"]
    label = lead1.name
    print(label)
    assert label == "aVL"

# def test_protobuf_ecg_lead_name_to_lead_name():
#     v1 = EcgLeadName.V1
#     v6 = EcgLeadName.V6
#     avl = EcgLeadName.aVL
#     sut_v1 = LeadName(v1)
#     sut_v6 = LeadName(v6)
#     sut_avl = LeadName(avl)
#     assert sut_v1 == LeadName.V1
#     assert sut_v6 == LeadName.V6
#     assert sut_avl == LeadName.aVL

# def test_protobuf_show_grid_to_show_grid():
#     show = Sh
# def test_lead_name_to_protobuf_ecg_lead_name():
#     v1 = LeadName.V1
#     v6 = LeadName.V6
#     avl = LeadName.aVL
#     random_signals = np.random.random(50)
#     test_signal: List[float] = random_signals.tolist()
#     ecg = EcgLead(lead_name=v1.name,signals=test_signal)
#     # ecg.lead_name = v1.value
#     # input_lead.lead_name = lead.lead_name.value
#     # sut_v1 = EcgLeadName.name(v1)
#     # sut_v1.value = v1
#
#     print(ecg.lead_name)
#     # sut_v6 = EcgLeadName(v6)
#     # sut_avl = EcgLeadName(avl)
#     # assert sut_v1 == EcgLeadName.V1
#     # assert sut_v6 == EcgLeadName.V6
#     # assert sut_avl == EcgLeadName.aVL
