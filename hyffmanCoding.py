import heapq
import os

class BinaryTree:
    def __init__(self, value, frequency):
        self.value = value
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __eq__(self, other):
        return self.frequency == other.frequency

    def __gt__(self, other):
        return self.frequency > other.frequency

class HuffmanCoding:
    def __init__(self, filePath):
        """
        Initialize HuffmanCoding with the given file path.
        :param filePath: Path to the input file for compression.
        """
        self.filePath = filePath
        self.heap = []
        self.codes = {}
        self.reverseCodes = {}

    def makeFrequencyDictionary(self, text):
        """
        Create a frequency dictionary for characters in the input text.
        :param text: Input text.
        :return: Frequency dictionary.
        """
        frequencyDict = {}
        for char in text:
            if char not in frequencyDict:
                frequencyDict[char] = 1
            else:
                frequencyDict[char] += 1
        return frequencyDict

    def buildHeap(self, frequencyDict):
        """
        Build a min-heap from the frequency dictionary.
        :param frequencyDict: Frequency dictionary.
        """
        for key in frequencyDict:
            frequency = frequencyDict[key]
            binaryTreeNode = BinaryTree(key, frequency)
            heapq.heappush(self.heap, binaryTreeNode)

    def buildTree(self):
        """
        Build the Huffman tree from the heap.
        """
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            totalFrequency = node1.frequency + node2.frequency
            newNode = BinaryTree(None, totalFrequency)
            newNode.left = node1
            newNode.right = node2
            heapq.heappush(self.heap, newNode)

    def buildCodesHelper(self, root, currentBits):
        """
        Helper function to build Huffman codes recursively.
        :param root: Current root node.
        :param currentBits: Current Huffman code.
        """
        if root is None:
            return
        if root.value is not None:
            self.codes[root.value] = currentBits
            self.reverseCodes[currentBits] = root.value
            return
        self.buildCodesHelper(root.left, currentBits + "0")
        self.buildCodesHelper(root.right, currentBits + "1")

    def buildCodes(self):
        """
        Build Huffman codes from the Huffman tree.
        """
        root = heapq.heappop(self.heap)
        self.buildCodesHelper(root, "")

    def getEncodedText(self, text):
        """
        Encode the input text using Huffman codes.
        :param text: Input text.
        :return: Encoded text.
        """
        encodedText = ""
        for char in text:
            encodedText += self.codes[char]
        return encodedText

    def getPaddedEncodedText(self, encodedText):
        """
        Pad the encoded text to ensure it is a multiple of 8 bits.
        :param encodedText: Encoded text.
        :return: Padded encoded text.
        """
        paddedAmount = 8 - (len(encodedText) % 8)
        for _ in range(paddedAmount):
            encodedText += '0'
        paddedInfo = "{0:08b}".format(paddedAmount)
        paddedEncodedText = paddedInfo + encodedText
        return paddedEncodedText

    def getBytesArray(self, paddedEncodedText):
        """
        Convert the padded encoded text to a bytes array.
        :param paddedEncodedText: Padded encoded text.
        :return: Bytes array.
        """
        bytesArray = [int(paddedEncodedText[i:i + 8], 2) for i in range(0, len(paddedEncodedText), 8)]
        return bytesArray

    def compression(self):
        
        # Open the input file in read and write mode
        with open(self.filePath, 'r+') as file:
            # Read the content of the file
            text = file.read()
            # Remove trailing whitespaces
            text = text.rstrip()

            # Create a frequency dictionary for characters in the input text
            frequencyDict = self.makeFrequencyDictionary(text)
            
            # Build a min-heap from the frequency dictionary
            self.buildHeap(frequencyDict)
            
            # Build the Huffman tree from the heap
            self.buildTree()
            
            # Build Huffman codes from the Huffman tree
            self.buildCodes()
            
            # Encode the input text using Huffman codes
            encodedText = self.getEncodedText(text)
            
            # Pad the encoded text to ensure it is a multiple of 8 bits
            paddedEncodedText = self.getPaddedEncodedText(encodedText)
            
            # Convert the padded encoded text to a bytes array
            bytesArray = self.getBytesArray(paddedEncodedText)

            # Get the file name and extension
            fileName, fileExtension = os.path.splitext(self.filePath)
            
            # Set the output path for the compressed file
            outputPath = fileName + ".bin"

            # Open the output file in binary write mode
            with open(outputPath, 'wb') as output:
                # Convert the bytes array to bytes and write it to the output file
                finalArray = bytes(bytesArray)
                output.write(finalArray)

        # Print a message indicating the compression is complete
        print('Compressed')
        
        # Return the path to the compressed file
        return outputPath


    def __removePadding(self, text):
        """
        Remove padding information from the text.
        :param text: Encoded text with padding.
        :return: Text without padding.
        """
        padded_info = text[:8]
        extra_padding = int(padded_info, 2)
        text = text[8:]
        text_after_padding = text[:-1 * extra_padding]
        return text_after_padding

    def __decodedText(self, text):
        """
        Decode the text using Huffman codes.
        :param text: Encoded text.
        :return: Decoded text.
        """
        decoded_text = ''
        current_bit = ''
        for bit in text:
            current_bit += bit
            # If the current bit sequence is in the reverseCodes, add the corresponding character to the decoded text
            if current_bit in self.reverseCodes:
                decoded_text += self.reverseCodes[current_bit]
                current_bit = ''
        return decoded_text

    def decompression(self, input_path):

        # Get the file name and extension from the input path
        filename, file_extension = os.path.splitext(input_path)
        
        # Set the output path for the decompressed file
        output_path = filename + '_decompressed' + '.txt'
        
        # Open the compressed file in binary read mode and the output file in write mode
        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            # Initialize an empty bit string to store binary representation of bytes
            bit_string = ''
            
            # Read a byte from the compressed file
            byte = file.read(1)
            
            # Loop through each byte until the end of the file
            while byte:
                # Convert the byte to its ASCII value
                byte = ord(byte)
                
                # Convert the ASCII value to binary and ensure it is 8 bits long
                bits = bin(byte)[2:].rjust(8, '0')
                
                # Append the binary representation to the bit string
                bit_string += bits
                
                # Read the next byte
                byte = file.read(1)
            
            # Remove padding information from the bit string
            actual_text = self.__removePadding(bit_string)
            
            # Decode the compressed bit string to obtain the decompressed text
            decompressed_text = self.__decodedText(actual_text)
            
            # Write the decompressed text to the output file
            output.write(decompressed_text)


# Example usage
huffmanCoder = HuffmanCoding("./sample.txt")
compressedPath = huffmanCoder.compression()
huffmanCoder.decompression(compressedPath)
