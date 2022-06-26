#!/usr/bin/env python3

from hashlib import new
import time
from bitstring import BitArray, BitStream, Bits
from crccheck.crc import Crc15Can
import binascii


def pretty_print(name, obj):
    if type(obj) is bool:
        data = '0b1' if obj else '0b0'
        return f"{name} [1]: {data}"
    elif type(obj) is int:
        return f"{name}: {obj}"
    else:
        return f"{name} [{len(obj)}]: {obj}"


class binary:
    with open("ImStuffed.bin", 'rb') as d:
        # data: Bits = Bits(d.read())
        data = BitStream(d)
    offset = 0
    messages = []
    consecutive = {
        "count": 0,
        "bit": None
    }

    def __init__(self):
        pass

    def get_bits(self, num):
        new_offset = self.offset + num
        val = self.data[self.offset:new_offset]

        self.offset = new_offset
        # print(f"Value: {val.bin}")
        # print(self)
        return val

    def get_bits_with_stuffing(self, num):
        ret = BitArray()
        while len(ret) != num:
            # Get bit at offset
            b = self.get_bits(1)
            if self.consecutive["bit"] == b:
                # If bit is consecutive, update count
                self.consecutive["count"] += 1
            else:
                # If bit is new, reset count
                self.consecutive["count"] = 1
                self.consecutive["bit"] = b

            # If 5 consecutive, next will be stuffing
            # Skip it and set it as consecutive - in case next is the same
            if self.consecutive["count"] == 5:
                skip = self.get_bits(1)
                self.consecutive["bit"] = skip
                self.consecutive["count"] = 1
                # print(f"Skipping {skip} at {self.offset}")
                # continue

            ret.append(b)
        return ret

    def get_bits_until(self, num):
        ret = BitArray()
        while self.data[self.offset] != num:
            ret.append(self.get_bits(1))
        return ret

    def __repr__(self):
        offset = pretty_print("Offset", self.offset)
        next_bits = pretty_print(
            "Next bits", self.data[self.offset:self.offset+16].bin)
        messages = "\n".join([msg.__repr__() for msg in self.messages])

        items = [
            offset,
            next_bits,
            # messages
        ]
        return "\n".join(items) + "\n"

    def parse_message(self):
        c = {}
        self.consecutive["bit"] = BitStream(1)
        self.consecutive["count"] = 1
        offset = self.offset
        SOF = self.get_bits_with_stuffing(1)
        Arbitration = self.get_bits_with_stuffing(12)
        Control = self.get_bits_with_stuffing(6)
        length = Control[2:6].uint
        if length > 8:
            print(f"cannot have length > 8 (is {length}")
            length = 8

        Data = self.get_bits_with_stuffing(length * 8)
        Crc = self.get_bits_with_stuffing(16)
        Ack = self.get_bits_with_stuffing(2)
        Eof = self.get_bits(7)
        Ifs = self.get_bits_until(0)
        c = CAN(len(self.messages) + 1, offset, SOF,
                Arbitration, Control, Data, Crc, Ack, Eof, Ifs)
        self.messages.append(c)

    def parse(self):
        while True:
        # for i in range(10):
            try:
                self.parse_message()
            except Exception as e:
                print(e)
                break
            except:
                break
            # time.sleep(1)

    def write(self):
        with open('out', 'wb') as f:
            for i, m in enumerate(self.messages):
                if i % 2 == 0:
                    continue
                f.write(m.data.bytes)

class CAN:
    def __init__(self, count: int, offset: int, SOF: Bits, Arbitration: Bits, Control: Bits, Data: Bits, CRC: Bits, ACK: Bits, EOF: Bits, IFS: Bits):
        self.count = count
        self.offset = offset
        self.SOF = SOF
        self.ID = Arbitration[:11]
        self.RTR = Arbitration[11:]
        self.IDE = Control[:1]
        self.reserved = Control[1:2]
        self.length = Control[2:6].uint
        self.data = Data
        self.CRC = CRC[:15]
        self.CRC_delim = CRC[15]
        self.ACK = ACK[0]
        self.ACK_delim = ACK[1]
        self.EOF = EOF
        self.IFS = IFS

        # print(self)

        # crc = Crc15Can.calc(Data.bytes)
        # print(f"0b{crc:>015b}\n{self.CRC}")

    def __repr__(self):
        items = [
            pretty_print("Message #", self.count),
            pretty_print("Offset", self.offset),
            pretty_print("Start of Frame", self.SOF),
            pretty_print("Identifier", self.ID),
            pretty_print("Remote Transmission Request", self.RTR),
            pretty_print("Identifier extension bit", self.IDE),
            pretty_print("Reserved", self.reserved),
            pretty_print("Data Length Code", self.length),
            pretty_print("Data", self.data),
            pretty_print("CRC", self.CRC),
            pretty_print("CRC Delimiter", self.CRC_delim),
            pretty_print("Ack", self.ACK),
            pretty_print("ACK Delimiter", self.ACK_delim),
            pretty_print("End of Frame", self.EOF),
            pretty_print("Inter-Frame Spacing", self.IFS),

            f"{binascii.b2a_uu(self.data.bytes)}"
        ]
        return "\n".join(items) + "\n"

    def __str__(self):
        return f"{binascii.b2a_uu(self.data.bytes)}"


bin = binary()
bin.parse()
bin.write()
# bin.parse_message()
# print(bin)
