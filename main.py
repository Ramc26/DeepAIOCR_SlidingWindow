import json
import logging
import os
import sys

from dotenv import load_dotenv

from classifier import ClassifyDocument
from demo_data import expected_labels, page_texts

logger = logging.getLogger(__name__)


def SummarizeAgainstExpected(results, expected):
    """Compare classifier output to demo ground truth."""
    if len(expected) != len(results):
        logger.warning(
            "main | expected_labels has %s entries, results has %s",
            len(expected),
            len(results),
        )

    matched_pages = []
    unmatched = []
    failed_pages = []

    for index, item in enumerate(results):
        page = item["page"]
        want = expected[index] if index < len(expected) else None

        if item["status"] != "success":
            failed_pages.append(page)
            continue

        if item["label"] == want:
            matched_pages.append(page)
        else:
            unmatched.append(
                {
                    "page": page,
                    "expected": want,
                    "got": item["label"],
                }
            )

    total = len(results)
    return {
        "total_pages": total,
        "matched_count": len(matched_pages),
        "unmatched_count": len(unmatched),
        "failed_count": len(failed_pages),
        "unmatched": unmatched,
        "failed_pages": failed_pages,
    }


def ConfigureLogging():
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
    )

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)
    root.addHandler(handler)


def main():
    load_dotenv()
    ConfigureLogging()

    document_id = "demo-proc-bundle-2026-104"
    page_count = len(page_texts)

    logger.info(
        "main | starting demo run document_id=%s pages=%s",
        document_id,
        page_count,
    )

    results = ClassifyDocument(
        page_texts=page_texts,
        document_id=document_id,
    )

    success_count = sum(1 for item in results if item["status"] == "success")
    logger.info(
        "main | demo run finished success=%s/%s — JSON results on stdout",
        success_count,
        page_count,
    )

    summary = SummarizeAgainstExpected(results, expected_labels)
    logger.info(
        "main | vs expected_labels: matched=%s/%s unmatched=%s failed=%s",
        summary["matched_count"],
        summary["total_pages"],
        summary["unmatched_count"],
        summary["failed_count"],
    )
    if summary["failed_pages"]:
        logger.error(
            "main | failed pages (no label): %s",
            summary["failed_pages"],
        )
    if summary["unmatched"]:
        for row in summary["unmatched"]:
            logger.warning(
                "main | page %s mismatch expected=%r got=%r",
                row["page"],
                row["expected"],
                row["got"],
            )
    else:
        logger.info("main | all successful pages match expected_labels")

    print(json.dumps(results, indent=2, ensure_ascii=False))
    print(
        json.dumps({"evaluation": summary}, indent=2, ensure_ascii=False),
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
