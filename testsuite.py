#!/usr/bin/python

# Runs various tests on stuff.

import simpleimap
import unittest

class TestParseSummaryData(unittest.TestCase):
    def setUp(self):
        # create an instance
        self.imap = simpleimap.SimpleImapSSL('imap.gmail.com')

    def testEmbeddedSubjectQuotes(self):
        """
        Tests a message with embedded double quotes in the Subject.

        >>> imap.uid('FETCH', 57454, '(UID ENVELOPE RFC822.SIZE INTERNALDATE)')
        """
        status, data = ('OK', ['49043 (UID 57454 RFC822.SIZE 2865 INTERNALDATE "27-Mar-2007 00:51:31 +0000" ENVELOPE ("Mon, 26 Mar 2007 17:51:28 -0700" "[XXXXXXX] anybody have some RIP dates for \\"Gone, But Not Forgotten\\"" (("YyyyyyY" NIL "ZzzzzzZZzzzz" "aaaaa.bbb")) ((NIL NIL "ccccccccccccc" "dddddddddddd.eee")) (("FfffffF" NIL "GgggggGGgggg" "hhhhh.iii")) (("Jjj Kkkkkkkkk Llll" NIL "mmmmmmmmmmm" "nnnnnnnnnnn.ooo")) NIL NIL NIL "<1174956688.961513.261310@p77g2000hsh.pppppppppppp.qqq>"))'])

        validresult = {'uid': 57454, 'envfrom': 'ZzzzzzZZzzzz@aaaaa.bbb', 'msgid': '<1174956688.961513.261310@p77g2000hsh.pppppppppppp.qqq>', 'envdate': 'Mon, 26 Mar 2007 17:51:28 -0700', 'date': '27-Mar-2007 00:51:31 +0000', 'size': 2865}

        result = self.imap.parse_summary_data(data)

        validkeys = sorted(validresult.keys())
        keys = sorted(result.keys())

        self.assertEqual(validkeys, keys, "wrong keys in result")

        for i in validkeys:
            self.assertEqual(validresult[i], result[i], "mismatch on %s" % i)

    def testEmbeddedSubjectFiveBackslashes(self):
        """
        Tests a message with five (!) backslashes in the Subject.
        >>> imap.uid('FETCH', 57455, '(UID ENVELOPE RFC822.SIZE INTERNALDATE)')
        """
        status, data = ('OK', ['49044 (UID 57455 RFC822.SIZE 554 INTERNALDATE "27-Mar-2007 01:16:26 +0000" ENVELOPE ("Mon, 26 Mar 2007 21:16:26 -0400" "s/Dicky\\\\\'s/Black Pearl Cafe/g" (("Aaaa Bbbbbb" NIL "ccccccc" "ddddd.eee")) (("Ffff Gggggg" NIL "hhhhhhh" "iiiii.jjj")) (("Kkkk Llllll" NIL "mmmmmmm" "nnnnn.ooo")) (("Pppppppp" NIL "qqqqqqqq" "rrrrrrrrrrrr.sss")) NIL NIL NIL "<4cb22bf90703261816hc33b998kad934bf355d9d737@tttt.uuuuu.vvv>"))'])

        validresult = {'uid': 57455, 'envfrom': 'ccccccc@ddddd.eee', 'msgid': '<4cb22bf90703261816hc33b998kad934bf355d9d737@tttt.uuuuu.vvv>', 'envdate': 'Mon, 26 Mar 2007 21:16:26 -0400', 'date': '27-Mar-2007 01:16:26 +0000', 'size': 554}

        result = self.imap.parse_summary_data(data)

        validkeys = sorted(validresult.keys())
        keys = sorted(result.keys())

        self.assertEqual(validkeys, keys, "wrong keys in result")

        for i in validkeys:
            self.assertEqual(validresult[i], result[i], "mismatch on %s" % i)

    def testInReplyTo(self):
        """
        Test a message with an in-reply-to, for the correct message ID.
        >>> imap.uid('FETCH', 17264, '(UID ENVELOPE RFC822.SIZE INTERNALDATE)')
        """
        status, data = ('OK', ['17258 (UID 17264 RFC822.SIZE 3346 INTERNALDATE "20-Aug-2005 17:58:38 +0000" ENVELOPE ("Sat, 20 Aug 2005 10:58:23 -0700 (PDT)" "[AAAaaaa] Re: Talk Pages" (("Bbbbb Cccccc" NIL "ddddd" "eeeeee.fff")) ((NIL NIL "ggggggggggggg" "hhhhhhhhhhhh.iii")) ((NIL NIL "jjjjjjjjjjjjj" "kkkkkkkkkkkk.lll")) ((NIL NIL "mmmmmmmmmmmmm" "nnnnnnnnnnnn.ooo")) NIL NIL "<f714681d0508191655339a8437@pppp.qqqqq.rrr>" "<Pine.LNX.4.53.0508201058130.909@ssssssss.tttttt.uuu>"))'])

        validresult = {'uid': 17264, 'envfrom': 'ddddd@eeeeee.fff', 'msgid': '<Pine.LNX.4.53.0508201058130.909@ssssssss.tttttt.uuu>', 'envdate': 'Sat, 20 Aug 2005 10:58:23 -0700 (PDT)', 'date': '20-Aug-2005 17:58:38 +0000', 'size': 3346}

        result = self.imap.parse_summary_data(data)

        validkeys = sorted(validresult.keys())
        keys = sorted(result.keys())

        self.assertEqual(validkeys, keys, "wrong keys in result")
        
        for i in validkeys:
            self.assertEqual(validresult[i], result[i], "mismatch on %s" % i)

if __name__ == '__main__':
    unittest.main()
