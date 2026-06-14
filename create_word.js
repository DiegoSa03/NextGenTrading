const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType, HeightRule, BorderStyle, VerticalAlign } = require("docx");

const border = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const borders = { top: border, bottom: border, left: border, right: border };

// Letter: 15840 DXA height, 0.7" margins top+bottom = 2016 DXA
// Usable height: 15840 - 2016 = 13824 DXA
// 18 rows: 13824 / 18 = 768 DXA each (use 720 for safety)
const rowHeight = 700;

const doc = new Document({
    styles: {
        default: { document: { run: { font: "Arial", size: 24 } } }
    },
    sections: [{
        properties: {
            page: {
                size: { width: 12240, height: 15840 },
                margin: { top: 1008, right: 1440, bottom: 1008, left: 1440 }
            }
        },
        children: [
            new Table({
                width: { size: 9360, type: WidthType.DXA },
                columnWidths: [2340, 3000, 4020],
                rows: [
                    // Title row
                    new TableRow({
                        height: { value: rowHeight, rule: HeightRule.ATLEAST },
                        children: [
                            new TableCell({
                                columnSpan: 3,
                                borders,
                                width: { size: 9360, type: WidthType.DXA },
                                verticalAlign: VerticalAlign.CENTER,
                                children: [
                                    new Paragraph({
                                        alignment: AlignmentType.CENTER,
                                        spacing: { before: 0, after: 0 },
                                        children: [new TextRun({ text: "MICRO 029", bold: true, size: 32 })]
                                    })
                                ]
                            })
                        ]
                    }),
                    // Header row
                    new TableRow({
                        height: { value: rowHeight, rule: HeightRule.ATLEAST },
                        children: [
                            new TableCell({
                                borders,
                                width: { size: 2340, type: WidthType.DXA },
                                verticalAlign: VerticalAlign.CENTER,
                                children: [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 0 }, children: [new TextRun({ text: "FECHA", bold: true, size: 24 })] })]
                            }),
                            new TableCell({
                                borders,
                                width: { size: 3000, type: WidthType.DXA },
                                verticalAlign: VerticalAlign.CENTER,
                                children: [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 0 }, children: [new TextRun({ text: "PRODUCIDO", bold: true, size: 24 })] })]
                            }),
                            new TableCell({
                                borders,
                                width: { size: 4020, type: WidthType.DXA },
                                verticalAlign: VerticalAlign.CENTER,
                                children: [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 0 }, children: [new TextRun({ text: "OBSERVACIONES", bold: true, size: 24 })] })]
                            })
                        ]
                    }),
                    // 16 empty rows
                    ...Array.from({ length: 16 }).map(() => new TableRow({
                        height: { value: rowHeight, rule: HeightRule.ATLEAST },
                        children: [
                            new TableCell({
                                borders,
                                width: { size: 2340, type: WidthType.DXA },
                                children: [new Paragraph({ spacing: { before: 0, after: 0 }, children: [new TextRun("")] })]
                            }),
                            new TableCell({
                                borders,
                                width: { size: 3000, type: WidthType.DXA },
                                children: [new Paragraph({ spacing: { before: 0, after: 0 }, children: [new TextRun("")] })]
                            }),
                            new TableCell({
                                borders,
                                width: { size: 4020, type: WidthType.DXA },
                                children: [new Paragraph({ spacing: { before: 0, after: 0 }, children: [new TextRun("")] })]
                            })
                        ]
                    }))
                ]
            })
        ]
    }]
});

Packer.toBuffer(doc).then((buffer) => {
    fs.writeFileSync("formato_micro_029.docx", buffer);
    console.log("Word created successfully");
});
